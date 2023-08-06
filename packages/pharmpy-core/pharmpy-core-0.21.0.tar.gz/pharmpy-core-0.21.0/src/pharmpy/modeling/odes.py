"""
:meta private:
"""

import sympy

import pharmpy.symbols
from pharmpy.parameter import Parameter
from pharmpy.statements import Assignment, Bolus, CompartmentalSystem, ExplicitODESystem, Infusion


def add_parameter(model, name):
    """Add an individual or pk parameter to a model"""
    _add_parameter(model, name)
    return model


def _add_parameter(model, name, init=0.1):
    pops = model.create_symbol(f'POP_{name}')
    pop_param = Parameter(pops.name, init=init, lower=0)
    model.parameters.add(pop_param)
    symb = model.create_symbol(name)
    ass = Assignment(symb, pop_param.symbol)
    model.statements.insert(0, ass)
    return symb


def explicit_odes(model):
    """Convert model from compartmental system to explicit ODE system
    or do nothing if it already has an explicit ODE system
    """
    statements = model.statements
    odes = statements.ode_system
    if isinstance(odes, CompartmentalSystem):
        eqs, ics = odes.to_explicit_odes()
        new = ExplicitODESystem(eqs, ics)
        statements[model.statements.index(odes)] = new
        model.statements = statements
        new.solver = odes.solver
    return model


def first_order_elimination(model):
    return model


def zero_order_elimination(model):
    """Sets elimination to zero order. Initial estimate for KM is set to 1% of smallest
    observation."""
    _do_michaelis_menten_elimination(model)
    obs = model.dataset.pharmpy.observations
    init = obs.min() / 100  # 1% of smallest observation
    model.parameters['POP_KM'].init = init
    model.parameters['POP_KM'].fix = True
    return model


def michaelis_menten_elimination(model):
    """Sets elimination to Michaelis-Menten. Initial estimate for CLMM is set to CL and KM is set to
    :math:`2*max(DV)`."""
    _do_michaelis_menten_elimination(model)
    return model


def mixed_mm_fo_elimination(model):
    """Sets elimination to mixed Michaelis-Menten and first order. Initial estimate for CLMM is set
    to CL/2 and KM is set to :math:`2*max(DV)`."""
    _do_michaelis_menten_elimination(model, combined=True)
    return model


def _do_michaelis_menten_elimination(model, combined=False):
    odes = model.statements.ode_system
    central = odes.find_central()
    output = odes.find_output()
    old_rate = odes.get_flow(central, output)
    numer, denom = old_rate.as_numer_denom()

    km_init, clmm_init = _get_mm_inits(model, numer, combined)

    km = _add_parameter(model, 'KM', init=km_init)
    clmm = _add_parameter(model, 'CLMM', init=clmm_init)

    if denom != 1:
        if combined:
            cl = numer
        vc = denom
    else:
        if combined:
            cl = _add_parameter(model, 'CL', clmm_init)
        vc = _add_parameter(model, 'VC')  # FIXME: decide better initial estimate
    if not combined:
        cl = 0

    amount = sympy.Function(central.amount.name)(pharmpy.symbols.symbol('t'))
    rate = (clmm * km / (km + amount / vc) + cl) / vc
    odes.add_flow(central, output, rate)
    model.statements.remove_symbol_definitions(numer.free_symbols, odes)
    model.remove_unused_parameters_and_rvs()
    return model


def _get_mm_inits(model, rate_numer, combined):
    pset, sset = model.parameters, model.statements
    clmm_init = sset.extract_params_from_symb(rate_numer.name, pset).init

    if combined:
        clmm_init /= 2

    dv_max = model.dataset.pharmpy.observations.max()
    km_init = dv_max * 2

    return km_init, clmm_init


def set_transit_compartments(model, n):
    """Set the number of transit compartments of model. Initial estimate for absorption rate is
    set the previous rate if available, otherwise it is set to the time of first observation/2
    is used."""
    statements = model.statements
    odes = statements.ode_system
    transits = odes.find_transit_compartments(statements)
    n = int(n)
    if len(transits) == n:
        pass
    elif len(transits) == 0:
        mdt_symb = _add_parameter(model, 'MDT', init=_get_absorption_init(model, 'MDT'))
        rate = n / mdt_symb
        comp = odes.find_dosing()
        dose = comp.dose
        comp.dose = None
        while n > 0:
            new_comp = odes.add_compartment(f'TRANSIT{n}')
            n -= 1
            odes.add_flow(new_comp, comp, rate)
            comp = new_comp
        comp.dose = dose
    elif len(transits) > n:
        nremove = len(transits) - n
        removed_symbols = set()
        trans, destination, flow = _find_last_transit(odes, transits)
        if n == 0:  # The dosing compartment will be removed
            dosing = odes.find_dosing()
            dose = dosing.dose
        remaining = set(transits)
        while nremove > 0:
            from_comp, from_flow = odes.get_compartment_inflows(trans)[0]
            odes.add_flow(from_comp, destination, from_flow)
            odes.remove_compartment(trans)
            remaining.remove(trans)
            removed_symbols |= flow.free_symbols
            trans = from_comp
            flow = from_flow
            nremove -= 1
        if n == 0:
            destination.dose = dose
        _update_numerators(model)
        statements.remove_symbol_definitions(removed_symbols, odes)
        model.remove_unused_parameters_and_rvs()
    else:
        nadd = n - len(transits)
        last, destination, rate = _find_last_transit(odes, transits)
        odes.remove_flow(last, destination)
        while nadd > 0:
            # new_comp = odes.add_compartment(f'TRANSIT{len(transits) + nadd}')
            new_comp = odes.add_compartment(f'TRANSIT{n - nadd + 1}')
            odes.add_flow(last, new_comp, rate)
            if rate.is_Symbol:
                ass = statements.find_assignment(rate.name)
                if ass is not None:
                    rate = ass.expression
            last = new_comp
            nadd -= 1
        odes.add_flow(last, destination, rate)
        _update_numerators(model)
    return model


def _find_last_transit(odes, transits):
    for trans in transits:
        destination, flow = odes.get_compartment_outflows(trans)[0]
        if destination not in transits:
            return trans, destination, flow


def _update_numerators(model):
    # update numerators for transit compartment rates
    statements = model.statements
    odes = statements.ode_system
    transits = odes.find_transit_compartments(statements)
    new_numerator = sympy.Integer(len(transits))
    for comp in transits:
        to_comp, rate = odes.get_compartment_outflows(comp)[0]
        numer, denom = rate.as_numer_denom()
        if numer.is_Integer and numer != new_numerator:
            new_rate = new_numerator / denom
            odes.add_flow(comp, to_comp, new_rate)
        elif numer.is_Symbol:
            ass = statements.find_assignment(numer.name)
            if ass is not None:
                ass_numer, ass_denom = ass.expression.as_numer_denom()
                if ass_numer.is_Integer and ass_numer != new_numerator:
                    new_rate = new_numerator / ass_denom
                    statements.reassign(numer, new_rate)


def add_lag_time(model):
    """Add lag time to the dose compartment of model. Initial estimate for lag time is set the
    previous lag time if available, otherwise it is set to the time of first observation/2 is
    used."""
    odes = model.statements.ode_system
    dosing_comp = odes.find_dosing()
    old_lag_time = dosing_comp.lag_time
    mdt_symb = _add_parameter(model, 'MDT', init=_get_absorption_init(model, 'MDT'))
    dosing_comp.lag_time = mdt_symb
    if old_lag_time:
        model.statements.remove_symbol_definitions(old_lag_time.free_symbols, odes)
        model.remove_unused_parameters_and_rvs()
    return model


def remove_lag_time(model):
    """Remove lag time from the dose compartment of model."""
    odes = model.statements.ode_system
    dosing_comp = odes.find_dosing()
    lag_time = dosing_comp.lag_time
    if lag_time:
        symbols = lag_time.free_symbols
        dosing_comp.lag_time = 0
        model.statements.remove_symbol_definitions(symbols, odes)
        model.remove_unused_parameters_and_rvs()
    return model


def zero_order_absorption(model):
    """Set or change to zero order absorption rate. Initial estimate for absorption rate is set
    the previous rate if available, otherwise it is set to the time of first observation/2 is
    used.

    Parameters
    ----------
    model : Model
        Model to set or change to first order absorption rate
    """
    statements = model.statements
    odes = statements.ode_system
    if not isinstance(odes, CompartmentalSystem):
        raise ValueError("Setting absorption is not supported for ExplicitODESystem")
    depot = odes.find_depot(statements)

    dose_comp = odes.find_dosing()
    symbols = dose_comp.free_symbols
    dose = dose_comp.dose
    if depot:
        to_comp, _ = odes.get_compartment_outflows(depot)[0]
        ka = odes.get_flow(depot, odes.find_central())
        odes.remove_compartment(depot)
        symbols |= ka.free_symbols
        to_comp.dose = dose
    else:
        to_comp = dose_comp
    statements.remove_symbol_definitions(symbols, odes)
    model.remove_unused_parameters_and_rvs()
    if not have_zero_order_absorption(model):
        add_zero_order_absorption(model, dose.amount, to_comp, 'MAT')
    return model


def first_order_absorption(model):
    """Set or change to first order absorption rate. Initial estimate for absorption rate is set
    the previous rate if available, otherwise it is set to the time of first observation/2 is used.

    Parameters
    ----------
    model : Model
        Model to set or change to bolus absorption rate
    """
    statements = model.statements
    odes = statements.ode_system
    if not isinstance(odes, CompartmentalSystem):
        raise ValueError("Setting absorption is not supported for ExplicitODESystem")
    depot = odes.find_depot(statements)

    dose_comp = odes.find_dosing()
    amount = dose_comp.dose.amount
    symbols = dose_comp.free_symbols
    if depot:
        dose_comp.dose = Bolus(depot.dose.amount)
    else:
        dose_comp.dose = None
    statements.remove_symbol_definitions(symbols, odes)
    model.remove_unused_parameters_and_rvs()
    if not depot:
        add_first_order_absorption(model, Bolus(amount), dose_comp)
    return model


def bolus_absorption(model):
    """Set or change to bolus absorption rate.

    Parameters
    ----------
    model : Model
        Model to set or change absorption rate
    """
    statements = model.statements
    odes = statements.ode_system
    if not isinstance(odes, CompartmentalSystem):
        raise ValueError("Setting absorption is not supported for ExplicitODESystem")
    depot = odes.find_depot(statements)
    if depot:
        to_comp, _ = odes.get_compartment_outflows(depot)[0]
        to_comp.dose = depot.dose
        ka = odes.get_flow(depot, odes.find_central())
        odes.remove_compartment(depot)
        symbols = ka.free_symbols
        statements.remove_symbol_definitions(symbols, odes)
        model.remove_unused_parameters_and_rvs()
    if have_zero_order_absorption(model):
        dose_comp = odes.find_dosing()
        old_symbols = dose_comp.free_symbols
        dose_comp.dose = Bolus(dose_comp.dose.amount)
        unneeded_symbols = old_symbols - dose_comp.dose.free_symbols
        statements.remove_symbol_definitions(unneeded_symbols, odes)
        model.remove_unused_parameters_and_rvs()
    return model


def seq_zo_fo_absorption(model):
    """Set or change to sequential zero order first order absorption rate. Initial estimate for
    absorption rate is set the previous rate if available, otherwise it is set to the time of
    first observation/2 is used.

    Parameters
    ----------
    model : Model
        Model to set or change absorption rate
    """
    statements = model.statements
    odes = statements.ode_system
    if not isinstance(odes, CompartmentalSystem):
        raise ValueError("Setting absorption is not supported for ExplicitODESystem")
    depot = odes.find_depot(statements)

    dose_comp = odes.find_dosing()
    have_ZO = have_zero_order_absorption(model)
    if depot and not have_ZO:
        add_zero_order_absorption(model, dose_comp.amount, depot, 'MDT')
    elif not depot and have_ZO:
        add_first_order_absorption(model, dose_comp.dose, dose_comp)
        dose_comp.dose = None
    elif not depot and not have_ZO:
        amount = dose_comp.dose.amount
        dose_comp.dose = None
        depot = add_first_order_absorption(model, amount, dose_comp)
        add_zero_order_absorption(model, amount, depot, 'MDT')
    return model


def have_zero_order_absorption(model):
    """Check if ode system describes a zero order absorption

    currently defined as having Infusion dose with rate not in dataset
    """
    odes = model.statements.ode_system
    dosing = odes.find_dosing()
    dose = dosing.dose
    if isinstance(dose, Infusion):
        if dose.rate is None:
            value = dose.duration
        else:
            value = dose.rate
        if isinstance(value, sympy.Symbol) or isinstance(value, str):
            name = str(value)
            if name not in model.dataset.columns:
                return True
    return False


def add_zero_order_absorption(model, amount, to_comp, parameter_name):
    """Add zero order absorption to a compartment. Initial estimate for absorption rate is set
    the previous rate if available, otherwise it is set to the time of first observation/2 is used.
    Disregards what is currently in the model.
    """
    mat_symb = _add_parameter(
        model, parameter_name, init=_get_absorption_init(model, parameter_name)
    )
    new_dose = Infusion(amount, duration=mat_symb * 2)
    to_comp.dose = new_dose


def add_first_order_absorption(model, dose, to_comp):
    """Add first order absorption
    Disregards what is currently in the model.
    """
    odes = model.statements.ode_system
    depot = odes.add_compartment('DEPOT')
    depot.dose = dose
    mat_symb = _add_parameter(model, 'MAT', _get_absorption_init(model, 'MAT'))
    odes.add_flow(depot, to_comp, 1 / mat_symb)
    return depot


def _get_absorption_init(model, param_name):
    try:
        if param_name == 'MDT':
            param_prev = model.statements.lag_time
        else:
            param_prev = model.statements.extract_params_from_symb(param_name, model.parameters)
        return param_prev.init
    except AttributeError:
        pass

    dt = model.dataset
    time_label = dt.pharmpy.idv_label
    obs = dt.pharmpy.observations
    time_min = obs.index.get_level_values(level=time_label).min()

    if param_name == 'MDT':
        return float(time_min) / 2
    elif param_name == 'MAT':
        return float(time_min) * 2


def set_peripheral_compartments(model, n):
    per = len(model.statements.ode_system.find_peripherals())
    if per < n:
        for _ in range(n - per):
            add_peripheral_compartment(model)
    elif per > n:
        for _ in range(per - n):
            remove_peripheral_compartment(model)
    return model


def add_peripheral_compartment(model):
    r"""Add a peripheral distribution compartment to model

    The rate of flow from the central to the peripheral compartment
    will be parameterized as QPn / VC where VC is the volume of the central compartment.
    The rate of flow from the peripheral to the central compartment
    will be parameterized as QPn / VPn where VPn is the volumne of the added peripheral
    compartment.

    Initial estimates:

    ==  ===================================================
    n
    ==  ===================================================
    1   :math:`\mathsf{CL} = \mathsf{CL'}`, :math:`\mathsf{VC} = \mathsf{VC'}`,
        :math:`\mathsf{QP1} = \mathsf{CL'}` and :math:`\mathsf{VP1} = \mathsf{VC'} \cdot 0.05`
    2   :math:`\mathsf{QP1} = \mathsf{QP1' / 2}`, :math:`\mathsf{VP1} = \mathsf{VP1'}`,
        :math:`\mathsf{QP2} = \mathsf{QP1' / 2}` and :math:`\mathsf{VP2} = \mathsf{VP1'}`
    ==  ===================================================

    """
    statements = model.statements
    odes = statements.ode_system
    per = odes.find_peripherals()
    n = len(per) + 1

    central = odes.find_central()
    output = odes.find_output()
    elimination_rate = odes.get_flow(central, output)
    cl, vc = elimination_rate.as_numer_denom()

    if n == 1:
        if vc == 1:
            kpc = _add_parameter(model, f'KPC{n}', init=0.1)
            kcp = _add_parameter(model, f'KCP{n}', init=0.1)
            peripheral = odes.add_compartment(f'PERIPHERAL{n}')
            odes.add_flow(central, peripheral, kcp)
            odes.add_flow(peripheral, central, kpc)
        else:
            full_cl = statements.full_expression_from_odes(cl)
            full_vc = statements.full_expression_from_odes(vc)
            pop_cl_candidates = full_cl.free_symbols & set(model.parameters.symbols)
            pop_cl = pop_cl_candidates.pop()
            pop_vc_candidates = full_vc.free_symbols & set(model.parameters.symbols)
            pop_vc = pop_vc_candidates.pop()
            pop_cl_init = model.parameters[pop_cl].init
            pop_vc_init = model.parameters[pop_vc].init
            qp_init = pop_cl_init
            vp_init = pop_vc_init * 0.05
    elif n == 2:
        per1 = per[0]
        from_rate = odes.get_flow(per1, central)
        qp1, vp1 = from_rate.as_numer_denom()
        full_qp1 = statements.full_expression_from_odes(qp1)
        full_vp1 = statements.full_expression_from_odes(vp1)
        pop_qp1_candidates = full_qp1.free_symbols & set(model.parameters.symbols)
        pop_qp1 = pop_qp1_candidates.pop()
        pop_vp1_candidates = full_vp1.free_symbols & set(model.parameters.symbols)
        pop_vp1 = pop_vp1_candidates.pop()
        pop_qp1_init = model.parameters[pop_qp1].init
        pop_vp1_init = model.parameters[pop_vp1].init
        model.parameters[pop_qp1].init = pop_qp1_init / 2
        qp_init = pop_qp1_init / 2
        vp_init = pop_vp1_init
    else:
        qp_init = 0.1
        vp_init = 0.1

    if vc != 1:
        qp = _add_parameter(model, f'QP{n}', init=qp_init)
        vp = _add_parameter(model, f'VP{n}', init=vp_init)
        peripheral = odes.add_compartment(f'PERIPHERAL{n}')
        odes.add_flow(central, peripheral, qp / vc)
        odes.add_flow(peripheral, central, qp / vp)

    return model


def remove_peripheral_compartment(model):
    r"""Remove a peripheral distribution compartment from model

    Initial estimates:

    ==  ===================================================
    n
    ==  ===================================================
    2   :math:`\mathsf{CL} = \mathsf{CL'}`,
        :math:`\mathsf{QP1} = \mathsf{CL'}` and :math:`\mathsf{VP1} = \mathsf{VC'} \cdot 0.05`
    3   :math:`\mathsf{QP1} = (\mathsf{QP1'} + \mathsf{QP2'}) / 2`,
        :math:`\mathsf{VP1} = \mathsf{VP1'} + \mathsf{VP2'}`
    ==  ===================================================

    """

    statements = model.statements
    odes = statements.ode_system
    peripherals = odes.find_peripherals()
    if peripherals:
        last_peripheral = peripherals[-1]
        central = odes.find_central()
        if len(peripherals) == 1:
            output = odes.find_output()
            elimination_rate = odes.get_flow(central, output)
            cl, vc = elimination_rate.as_numer_denom()
            from_rate = odes.get_flow(last_peripheral, central)
            qp1, vp1 = from_rate.as_numer_denom()
            full_cl = statements.full_expression_from_odes(cl)
            full_vc = statements.full_expression_from_odes(vc)
            full_qp1 = statements.full_expression_from_odes(qp1)
            full_vp1 = statements.full_expression_from_odes(vp1)
            pop_cl_candidates = full_cl.free_symbols & set(model.parameters.symbols)
            pop_cl = pop_cl_candidates.pop()
            pop_vc_candidates = full_vc.free_symbols & set(model.parameters.symbols)
            pop_vc = pop_vc_candidates.pop()
            pop_qp1_candidates = full_qp1.free_symbols & set(model.parameters.symbols)
            pop_qp1 = pop_qp1_candidates.pop()
            pop_vp1_candidates = full_vp1.free_symbols & set(model.parameters.symbols)
            pop_vp1 = pop_vp1_candidates.pop()
            pop_vc_init = model.parameters[pop_vc].init
            pop_cl_init = model.parameters[pop_cl].init
            pop_qp1_init = model.parameters[pop_qp1].init
            pop_vp1_init = model.parameters[pop_vp1].init
            new_vc_init = pop_vc_init + pop_qp1_init / pop_cl_init * pop_vp1_init
            model.parameters[pop_vc].init = new_vc_init
        elif len(peripherals) == 2:
            first_peripheral = peripherals[0]
            from1_rate = odes.get_flow(first_peripheral, central)
            qp1, vp1 = from1_rate.as_numer_denom()
            from2_rate = odes.get_flow(last_peripheral, central)
            qp2, vp2 = from2_rate.as_numer_denom()
            full_qp2 = statements.full_expression_from_odes(qp2)
            full_vp2 = statements.full_expression_from_odes(vp2)
            full_qp1 = statements.full_expression_from_odes(qp1)
            full_vp1 = statements.full_expression_from_odes(vp1)
            pop_qp2_candidates = full_qp2.free_symbols & set(model.parameters.symbols)
            pop_qp2 = pop_qp2_candidates.pop()
            pop_vp2_candidates = full_vp2.free_symbols & set(model.parameters.symbols)
            pop_vp2 = pop_vp2_candidates.pop()
            pop_qp1_candidates = full_qp1.free_symbols & set(model.parameters.symbols)
            pop_qp1 = pop_qp1_candidates.pop()
            pop_vp1_candidates = full_vp1.free_symbols & set(model.parameters.symbols)
            pop_vp1 = pop_vp1_candidates.pop()
            pop_qp2_init = model.parameters[pop_qp2].init
            pop_vp2_init = model.parameters[pop_vp2].init
            pop_qp1_init = model.parameters[pop_qp1].init
            pop_vp1_init = model.parameters[pop_vp1].init
            new_qp1_init = (pop_qp1_init + pop_qp2_init) / 2
            new_vp1_init = pop_vp1_init + pop_vp2_init
            model.parameters[pop_qp1].init = new_qp1_init
            model.parameters[pop_vp1].init = new_vp1_init

        symbols = odes.get_flow(central, last_peripheral).free_symbols
        symbols |= odes.get_flow(last_peripheral, central).free_symbols
        odes.remove_compartment(last_peripheral)
        model.statements.remove_symbol_definitions(symbols, odes)
        model.remove_unused_parameters_and_rvs()
    return model


def set_ode_solver(model, solver):
    odes = model.statements.ode_system
    odes.solver = solver
    return model
