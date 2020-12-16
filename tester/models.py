from django.db import models

class Submission(models.Model):
    submission_time = models.DateTimeField(help_text="When this answer to coding assignment was tested as working")
    assignment_name = models.CharField(max_length=256, default='',
        help_text="The name of the coding assignment this is a submission for")
    submission_endpoint_address = models.URLField(max_length=2048,
        help_text="The address (endpoint) where this answer was tested")
    applicant_address = models.EmailField(max_length=2048,
        help_text="Applicant's contact email address")
    submission_code_address = models.URLField(max_length=2048,
        help_text="Address where the code implementing the submission can be found")
    def __str__(s):
        return "%s @%s" % (s.submission_endpoint_address, s.submission_time)

class PassedTest(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE)
    test_input = models.TextField()
    test_output = models.TextField()
    def __str__(s):
        return "%s <- %s" % (s.submission, s.test_input)
