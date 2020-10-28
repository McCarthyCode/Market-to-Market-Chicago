from mtm.settings import STAGE

def stage(request):
    return {'STAGE': STAGE}
