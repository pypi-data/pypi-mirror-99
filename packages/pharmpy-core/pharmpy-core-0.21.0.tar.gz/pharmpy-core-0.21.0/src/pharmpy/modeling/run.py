import pharmpy.methods.common
import pharmpy.methods.modelfit
import pharmpy.model
import pharmpy.results


def fit(models):
    if isinstance(models, pharmpy.model.Model):
        models = [models]
        single = True
    else:
        single = False
    tool = pharmpy.methods.modelfit.Modelfit(models)
    tool.run()
    if single:
        return models[0]
    else:
        return models


def create_results(path, **kwargs):
    res = pharmpy.methods.common.create_results(path, **kwargs)
    return res


def read_results(path):
    res = pharmpy.results.read_results(path)
    return res
