from django.http import HttpResponse


def rollbar_test_view(request):
    a = None
    # Intentional error to trigger Rollbar reporting
    a.hello()  # type: ignore[attr-defined]
    return HttpResponse("Hello, world. You're at the rollbar test.")

