import csv
from collections import defaultdict, OrderedDict
from unidecode import unidecode

from django import forms
import django.forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.forms.utils import ErrorList
from django.utils.html import format_html
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
import six

from wagtail.admin.forms import WagtailAdminPageForm
from wagtail.contrib.forms.forms import FormBuilder
from .blocks import SkipState, VALID_SKIP_LOGIC, VALID_SKIP_SELECTORS
from .widgets import NaturalDateInput

CHARACTER_COUNT_CHOICE_LIMIT = 512


class CharacterCountWidget(forms.TextInput):
    class Media:
        js = ('js/widgets/character_count.js',)

    def render(self, name, value, attrs=None, renderer=None):
        max_length = self.attrs['maxlength']
        maximum_text = _('Maximum: {max_length}').format(max_length=max_length)
        return format_html(
            u'{}<span>{}</span>',
            super(CharacterCountWidget, self).render(name, value, attrs),
            maximum_text,
        )


class MultiLineWidget(forms.Textarea):
    def render(self, name, value, attrs=None, renderer=None):
        return format_html(
            u'{}<span>{}</span>',
            super(MultiLineWidget, self).render(name, value, attrs),
            _('No limit'),
        )


class CharacterCountMixin(object):
    max_length = CHARACTER_COUNT_CHOICE_LIMIT

    def __init__(self, *args, **kwargs):
        self.max_length = kwargs.pop('max_length', self.max_length)
        super(CharacterCountMixin, self).__init__(*args, **kwargs)
        self.error_messages['max_length'] = _(
            'This field can not be more than {max_length} characters long'
        ).format(max_length=self.max_length)

    def validate(self, value):
        super(CharacterCountMixin, self).validate(value)
        if len(value) > self.max_length:
            raise ValidationError(
                self.error_messages['max_length'],
                code='max_length', params={'value': value},
            )


class CharacterCountMultipleChoiceField(
        CharacterCountMixin, forms.MultipleChoiceField):
    """ Limit character count for Multi choice fields """


class CharacterCountChoiceField(
        CharacterCountMixin, forms.ChoiceField):
    """ Limit character count for choice fields """


class CharacterCountCheckboxSelectMultiple(
        CharacterCountMixin, forms.CheckboxSelectMultiple):
    """ Limit character count for checkbox fields """


class CharacterCountCheckboxInput(
        CharacterCountMixin, forms.CheckboxInput):
    """ Limit character count for checkbox fields """


class FormsFormBuilder(FormBuilder):
    def create_singleline_field(self, field, options):
        options['widget'] = CharacterCountWidget
        return super(FormsFormBuilder, self).create_singleline_field(
            field, options)

    def create_multiline_field(self, field, options):
        options['widget'] = MultiLineWidget
        return forms.CharField(**options)

    def create_date_field(self, field, options):
        options['widget'] = NaturalDateInput
        return super(
            FormsFormBuilder, self).create_date_field(field, options)

    def create_datetime_field(self, field, options):
        options['widget'] = NaturalDateInput
        return super(
            FormsFormBuilder, self).create_datetime_field(field, options)

    def create_positive_number_field(self, field, options):
        return forms.DecimalField(min_value=0, **options)

    def create_dropdown_field(self, field, options):
        options['choices'] = map(
            lambda x: (x.strip(), x.strip()),
            field.choices.split(','))
        return CharacterCountChoiceField(**options)

    def create_radio_field(self, field, options):
        options['choices'] = map(
            lambda x: (x.strip(), x.strip()),
            field.choices.split(','))
        return CharacterCountChoiceField(widget=forms.RadioSelect, **options)

    def create_checkboxes_field(self, field, options):
        options['choices'] = [
            (x.strip(), x.strip()) for x in field.choices.split(',')
        ]
        options['initial'] = [
            x.strip() for x in field.default_value.split(',')
        ]
        return CharacterCountMultipleChoiceField(
            widget=forms.CheckboxSelectMultiple, **options)

    def create_email_field(self, field, options):
        return django.forms.EmailField(**options)

    def create_url_field(self, field, options):
        return django.forms.URLField(**options)

    def create_number_field(self, field, options):
        return django.forms.DecimalField(**options)

    def create_checkbox_field(self, field, options):
        return django.forms.BooleanField(**options)

    def create_hidden_field(self, field, options):
        return django.forms.CharField(
            **options, widget=django.forms.HiddenInput)

    FIELD_TYPES = {
        'singleline': create_singleline_field,
        'multiline': create_multiline_field,
        'date': create_date_field,
        'datetime': create_datetime_field,
        'email': create_email_field,
        'url': create_url_field,
        'number': create_number_field,
        'positive_number': create_positive_number_field,
        'dropdown': create_dropdown_field,
        'radio': create_radio_field,
        'checkboxes': create_checkboxes_field,
        'checkbox': create_checkbox_field,
        'hidden': create_hidden_field,
    }

    @property
    def formfields(self):
        formfields = OrderedDict()

        for field in self.fields:
            options = self.get_field_options(field)
            if field.field_type in self.FIELD_TYPES:
                method = getattr(self,
                                 self.FIELD_TYPES[field.field_type].__name__)
                formfields[field.clean_name] = method(field, options)
            else:
                raise Exception("Unrecognised field type: " + field.field_type)

        return formfields


class CSVGroupCreationForm(forms.ModelForm):
    """Create group with initial users supplied via CSV file."""
    csv_file = forms.FileField(
        label=_('CSV file'),
        help_text=_('Please attach a CSV file with the first column containing'
                    ' usernames of users that you want to be added to '
                    'this group.'))

    class Meta:
        model = Group
        fields = ("name",)

    def clean_csv_file(self):
        """Read CSV file and save the users to self.initial_users."""
        csv_file = self.cleaned_data['csv_file']

        # Sniff CSV file
        try:
            dialect = csv.Sniffer().sniff(csv_file.read(1024))
        except csv.Error:
            raise forms.ValidationError(_('Uploaded file does not appear to be'
                                          ' in CSV format.'))

        csv_file.seek(0)

        # Instantiate CSV Reader
        csv_file_reader = csv.reader(csv_file, dialect)

        # Check whether file has a header
        try:
            if csv.Sniffer().has_header(csv_file.read(1024)):
                next(csv_file_reader)  # Skip the header
        except csv.Error:
            raise forms.ValidationError(_('Uploaded file does not appear to be'
                                          ' in CSV format.'))

        # Gather all usernames from the CSV file.
        usernames = set()
        for row in csv_file_reader:
            try:
                username = row[0]
            except IndexError:
                # Skip empty row
                continue
            else:
                # Skip empty username field
                if username:
                    usernames.add(username)

        if not usernames:
            raise forms.ValidationError(_('Your CSV file does not appear to '
                                          'contain any usernames.'))

        queryset = get_user_model().objects.filter(username__in=usernames)
        difference = usernames - set(queryset.values_list('username',
                                                          flat=True))
        if difference:
            raise forms.ValidationError(_('Please make sure your file contains'
                                          ' valid data. '
                                          'Those usernames do not exist: '
                                          '"%s".') % '", "'.join(difference))

        # Store users temporarily as a property so we can
        # add them when user calls save() on the form.
        self.__initial_users = queryset

    def save(self, *args, **kwargs):
        """Save the group instance and add initial users to it."""
        # Save the group instance
        group = super(CSVGroupCreationForm, self).save(*args, **kwargs)

        # Add users to the group
        group.user_set.add(*self.__initial_users)


class BaseMoloForm(WagtailAdminPageForm):
    def clean(self):
        cleaned_data = super(BaseMoloForm, self).clean()

        question_data = {}
        for form in self.formsets.get(self.form_field_name):
            form.is_valid()
            question_data[form.cleaned_data.get('ORDER')] = form

        field_names = []
        for form in question_data.values():
            data = form.cleaned_data
            if data and data.get('label'):
                field_name = str(
                    slugify(six.text_type(unidecode(data.get('label'))))
                )
                if field_name in field_names:
                    if 'label' not in form._errors:
                        form._errors['label'] = []
                    form._errors['label'].append(_(
                        "This question appears elsewhere in the form. Please "
                        "rephrase one of the questions."))
                field_names.append(field_name)

        for form in question_data.values():
            self._clean_errors = {}
            if form.is_valid():
                data = form.cleaned_data
                is_checkbox = data['field_type'] == 'checkbox'
                if data['field_type'] in VALID_SKIP_LOGIC and not is_checkbox:
                    choices_length = 0
                    for i, logic in enumerate(data.get('skip_logic')):
                        if not logic.value['choice']:
                            self.add_stream_field_error(
                                i,
                                'choice',
                                _('This field is required.'),
                            )
                        else:
                            choices_length += len(logic.value['choice'])

                    if choices_length > CHARACTER_COUNT_CHOICE_LIMIT:
                        err = 'The combined choices\' maximum characters ' \
                              'limit has been exceeded ({max_limit} '\
                              'character(s)).'
                        self.add_form_field_error(
                            'field_type',
                            _(err).format(
                                max_limit=CHARACTER_COUNT_CHOICE_LIMIT),
                        )

                if is_checkbox and not len(data.get('skip_logic')) == 2:
                    err = _(
                        'Checkbox must include only 2 Answer Options.'
                        ' True and False in that order')

                    form._errors['field_type'] = [err] if not \
                        form._errors.get('field_type') \
                        else form._errors['field_type'].append(err)

                for i, logic in enumerate(data.get('skip_logic')):
                    if logic.value['skip_logic'] == SkipState.FORM:
                        form = logic.value.get('form')
                        self.clean_form(i, form)
                    if logic.value['skip_logic'] == SkipState.QUESTION:
                        target = question_data.get(logic.value.get('question'))
                        target_data = target.cleaned_data
                        self.clean_question(i, data, target_data)
                if self.clean_errors:
                    form._errors = self.clean_errors

            elif self.form_cant_have_skip_errors(form):
                del form._errors['skip_logic']

        return cleaned_data

    def save(self, commit):
        # Tidy up the skip logic when field cant have skip logic
        for form in self.formsets[self.form_field_name]:
            field_type = form.instance.field_type
            if field_type not in VALID_SKIP_SELECTORS:
                if field_type != 'checkboxes':
                    form.instance.skip_logic = []
                else:
                    for skip_logic in form.instance.skip_logic:
                        skip_logic.value['skip_logic'] = SkipState.NEXT
                        skip_logic.value['question'] = None
                        skip_logic.value['form'] = None
            elif field_type == 'checkbox':
                for skip_logic in form.instance.skip_logic:
                    skip_logic.value['choice'] = ''

        return super(BaseMoloForm, self).save(commit)

    def clean_question(self, position, *args):
        self.clean_formset_field('question', position, *args)

    def clean_form(self, position, *args):
        self.clean_formset_field('form', position, *args)

    def clean_formset_field(self, field, position, *args):
        for method in getattr(self, field + '_clean_methods', []):
            error = getattr(self, method)(*args)
            if error:
                self.add_stream_field_error(position, field, error)

    def form_cant_have_skip_errors(self, form):
        return (
            form.has_error('skip_logic') and
            form.cleaned_data.get('field_type') not in VALID_SKIP_LOGIC
        )

    def check_doesnt_loop_to_self(self, form):
        if form and self.instance == form:
            return _('Cannot skip to self, please select a different form.')

    def add_form_field_error(self, field, message):
        if field not in self._clean_errors:
            self._clean_errors[field] = list()
        self._clean_errors[field].append(message)

    def add_stream_field_error(self, position, field, message):
        if position not in self._clean_errors:
            self._clean_errors[position] = defaultdict(list)
        self._clean_errors[position][field].append(message)

    @property
    def clean_errors(self):
        if self._clean_errors.keys():
            params = {
                key: ErrorList(
                    [ValidationError('Error in form', params=value)]
                )
                for key, value in self._clean_errors.items()
                if isinstance(key, int)
            }
            errors = {
                key: ValidationError(value)
                for key, value in self._clean_errors.items()
                if isinstance(key, six.string_types)
            }
            errors.update({
                'skip_logic': ErrorList([ValidationError(
                    'Skip Logic Error',
                    params=params,
                )])
            })
            return errors


class MoloForm(BaseMoloForm):
    form_field_name = 'form_fields'
    form_clean_methods = [
        'check_doesnt_loop_to_self',
        'check_doesnt_link_to_personalised_form',
    ]

    def check_doesnt_link_to_personalised_form(self, form):
        try:
            segment = form.personalisableform.segment
        except AttributeError:
            pass
        else:
            # Can only link a form without a segments
            if segment:
                return _('Cannot select a form with a segment.')


class PersonalisableMoloForm(BaseMoloForm):
    form_field_name = 'personalisable_form_fields'
    form_clean_methods = [
        'check_doesnt_loop_to_self',
        'check_form_link_valid',
    ]

    question_clean_methods = [
        'check_question_segment_ok',
    ]

    def check_question_segment_ok(self, question, target):
        # Cannot link from None to segment, but can link from segment to None
        current_segment = question.get('segment')
        linked_segment = target.get('segment')
        if linked_segment and (linked_segment != current_segment):
            return _('Cannot link to a question with a different segment.')

    def check_form_link_valid(self, form):
        try:
            segment = form.personalisableform.segment
        except AttributeError:
            pass
        else:
            # Can only link a form without segments or the same segment
            if segment and segment != self.instance.segment:
                return _('Cannot select a form with a different segment.')
