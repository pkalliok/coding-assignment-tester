from django.db import models

class Submission(models.Model):
    submission_time = models.DateTimeField(help_text="When this answer to coding assignment was tested as working")
    submission_endpoint_address = models.URLField(max_length=2048,
        help_text="The address (endpoint) where this answer was tested")
    applicant_address = models.EmailField(max_length=2048,
        help_text="Applicant's contact email address")
    submission_code_address = models.URLField(max_length=2048,
        help_text="Address where the code implementing the submission can be found")

class PassedTest(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    test_input = models.TextField()
    test_output = models.TextField()

