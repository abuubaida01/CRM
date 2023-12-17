from django.conf import settings

class StatsDebugMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response 

  def __call__(self, request):
    print("\nPassed Stats Debug Middleware....\n ")
    response = self.get_response(request)
    return response