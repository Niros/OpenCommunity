from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from issues import models
from issues.models import ProposalType
import floppyforms as forms
from ocd.formfields import HTMLArea


class BaseIssueForm(forms.ModelForm):
    class Meta:
        model = models.Issue
        fields = (
                   'title',
                   'abstract',
                   )

        widgets = {
            'title': forms.TextInput,
            'abstract': HTMLArea,
        }


class CreateIssueForm(BaseIssueForm):

    def __init__(self, *args, **kwargs):

        super(CreateIssueForm, self).__init__(*args, **kwargs)

        initial = {'type': ProposalType.ADMIN}

        self.new_proposal = CreateProposalBaseForm(prefix='proposal',
                                   data=self.data if self.is_bound else None,
                                   initial=initial)
        self.new_proposal.fields['type'].required = False

    def is_valid(self):
        valid = super(CreateIssueForm, self).is_valid()
        if self.data.get('proposal-type') == '':
            return valid
        return self.new_proposal.is_valid() and valid

    def save(self, commit=True):
        o = super(CreateIssueForm, self).save(commit)
        if self.data.get('proposal-type') != '':
            self.new_proposal.instance.issue = o
            self.new_proposal.instance.created_by = o.created_by
            self.new_proposal.save()
        return o


class UpdateIssueForm(BaseIssueForm):
    def __init__(self, *args, **kwargs):
#         self.helper = FormHelper()
# 
#         self.helper.add_input(Submit('submit', _('Update')))

        super(UpdateIssueForm, self).__init__(*args, **kwargs)
        self.helper.form_tag = True


class AddAttachmentBaseForm(forms.ModelForm):
    class Meta:
        model = models.IssueAttachment
        fields = (
                   'title',
                   'file',
                   )

    def clean_file(self):

        file_obj = self.cleaned_data['file']

        if len(file_obj.name.split('.')) == 1:
            raise forms.ValidationError(_("File type is not allowed!"))

        if file_obj.name.split('.')[-1] not in settings.UPLOAD_ALLOWED_EXTS:
            raise forms.ValidationError(_("File type is not allowed!"))

        return file_obj



class AddAttachmentForm(AddAttachmentBaseForm):
    submit_button_text = _('Upload')

    def __init__(self, *args, **kwargs):
#         self.helper = FormHelper()
# 
#         self.helper.add_input(Submit('submit', self.submit_button_text))

        super(AddAttachmentForm, self).__init__(*args, **kwargs)


class CreateProposalBaseForm(forms.ModelForm):

    class Meta:
        model = models.Proposal
        fields = (
                   'type',
                   'title',
                   'content',
                   'assigned_to',
                   'due_by',
                   )
        widgets = {
            'type': forms.Select,
            'title': forms.TextInput,
            'content': HTMLArea,
            'assigned_to': forms.TextInput,
            'due_by': forms.DateInput,
        }


class CreateProposalForm(CreateProposalBaseForm):

    submit_button_text = _('Create')

    def __init__(self, *args, **kwargs):
#         self.helper = FormHelper()
# 
#         self.helper.add_input(Submit('submit', self.submit_button_text))

        super(CreateProposalForm, self).__init__(*args, **kwargs)
        self.fields['type'].initial = ProposalType.ADMIN


class EditProposalForm(CreateProposalForm):
    submit_button_text = _('Save')


class EditProposalTaskForm(EditProposalForm):

    class Meta:
        model = models.Proposal
        fields = (
                   'assigned_to',
                   'due_by',
                   )


class CreateIssueCommentForm(forms.ModelForm):

    submit_label = _('Add')
    form_id = "add-comment"

    class Meta:
        model = models.IssueComment
        fields = (
                   'content',
                   )

    def __init__(self, *args, **kwargs):
#         self.helper = FormHelper()
#         if self.form_id:
#             self.helper.form_id = self.form_id

#         self.helper.add_input(Submit('submit', self.submit_label))

        super(CreateIssueCommentForm, self).__init__(*args, **kwargs)


class EditIssueCommentForm(CreateIssueCommentForm):

    submit_label = _('Save')
    form_id = None
