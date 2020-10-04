from django.contrib import admin
from .models import Submission, PassedTest

class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('submission_time', 'assignment_name',
            'submission_endpoint_address', 'applicant_address',
            'submission_code_address')
    actions = ('download_csv',)

    def download_csv(self, request, qset):
        import csv, django.http
        res = django.http.HttpResponse(content_type='text/csv')
        res['Content-Disposition'] = 'attachment; filename=submissions.csv'
        w = csv.writer(res)
        w.writerow(('Time', 'Assignment', 'Endpoint', 'Applicant', 'Source'))
        for rec in qset: w.writerow((rec.submission_time,
                rec.assignment_name, rec.submission_endpoint_address,
                rec.applicant_address, rec.submission_code_address))
        return res

    download_csv.short_description = 'Download selected rows as CSV file'

admin.site.register(Submission, SubmissionAdmin)
admin.site.register(PassedTest)
