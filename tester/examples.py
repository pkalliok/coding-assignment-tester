from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import json

@csrf_exempt
def nth_fibo(request):
    n = json.loads(request.body)
    a, b = 0, 1
    for i in range(n): a, b = a+b, a
    return JsonResponse(a, safe=False)

