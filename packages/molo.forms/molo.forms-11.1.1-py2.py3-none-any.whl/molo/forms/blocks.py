from django import forms
from django.templatetags.static import static
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel


class SkipState:
    NEXT = 'next'
    END = 'end'
    QUESTION = 'question'
    FORM = 'form'


VALID_SKIP_SELECTORS = ['radio', 'checkbox', 'dropdown']


VALID_SKIP_LOGIC = VALID_SKIP_SELECTORS + ['checkboxes']


class SkipLogicField(StreamField):
    def __init__(self, *args, **kwargs):
        args = [SkipLogicStreamBlock([('skip_logic', SkipLogicBlock())])]
        kwargs.update({
            'verbose_name': _('Answer options'),
            'blank': True,
            # Help text is used to display a message for a specific field type.
            # If different help text is required each type might need to be
            # wrapped in a <div id="<field-type>-helptext"> for the frontend
            'help_text': mark_safe(
                '<strong>{}</strong>'.format(
                    _('Checkbox must include only 2 Answer Options. '
                      'True and False in that order.')
                )
            )
        })
        super(SkipLogicField, self).__init__(*args, **kwargs)


class SkipLogicStreamPanel(StreamFieldPanel):
    def bind_to_model(self, model):
        model_class = super(SkipLogicStreamPanel, self).bind_to_model(model)
        model_class.classname = 'skip-logic'
        return model_class


class SelectAndHiddenWidget(forms.MultiWidget):
    def __init__(self, *args, **kwargs):
        widgets = [forms.HiddenInput, forms.Select]
        super(SelectAndHiddenWidget, self).__init__(
            widgets=widgets,
            *args,
            **kwargs
        )

    def decompress(self, value):
        return [value, None]

    def value_from_datadict(self, *args):
        value = super(SelectAndHiddenWidget, self).value_from_datadict(*args)
        return value[1]


class SkipLogicStreamBlock(blocks.StreamBlock):
    @property
    def media(self):
        media = super(SkipLogicStreamBlock, self).media
        css = media._css
        css.update({'all': [static('css/blocks/skiplogic.css')]})
        js = media._js + [static('js/blocks/skiplogic_stream.js')]
        media = forms.Media(css=css, js=js)
        return media

    def js_initializer(self):
        init = super(SkipLogicStreamBlock, self).js_initializer()
        return 'SkipLogic' + init


class QuestionSelectBlock(blocks.IntegerBlock):
    def __init__(self, *args, **kwargs):
        super(QuestionSelectBlock, self).__init__(*args, **kwargs)
        self.field.widget = SelectAndHiddenWidget()


class SkipLogicBlock(blocks.StructBlock):
    choice = blocks.CharBlock(required=False)
    skip_logic = blocks.ChoiceBlock(
        choices=[
            (SkipState.NEXT, _('Next default question')),
            (SkipState.END, _('End of form')),
            (SkipState.QUESTION, _('Another question')),
            (SkipState.FORM, _('Another form')),
        ],
        default=SkipState.NEXT,
        required=True,
    )
    form = blocks.PageChooserBlock(
        target_model='forms.MoloFormPage',
        required=False,
    )
    question = QuestionSelectBlock(
        required=False,
        help_text=_(
            ('Please save the form as a draft to populate or update '
             'the list of questions.')
        ),
    )

    @property
    def media(self):
        return forms.Media(js=[static('js/blocks/skiplogic.js')])

    def js_initializer(self):
        opts = {'validSkipSelectors': VALID_SKIP_SELECTORS}
        return "SkipLogic(%s)" % blocks.utils.js_dict(opts)

    def clean(self, value):
        cleaned_data = super(SkipLogicBlock, self).clean(value)
        logic = cleaned_data['skip_logic']
        if logic == SkipState.FORM:
            if not cleaned_data['form']:
                raise ValidationError(
                    'A Form must be selected to progress to.',
                    params={'form': [_('Please select a form.')]}
                )
            cleaned_data['question'] = None

        if logic == SkipState.QUESTION:
            if not cleaned_data['question']:
                raise ValidationError(
                    'A Question must be selected to progress to.',
                    params={'question': [_('Please select a question.')]}
                )
            cleaned_data['form'] = None

        if logic in [SkipState.END, SkipState.NEXT]:
            cleaned_data['form'] = None
            cleaned_data['question'] = None

        return cleaned_data


class RuleSelectBlock(blocks.CharBlock):
    def __init__(self, *args, **kwargs):
        super(RuleSelectBlock, self).__init__(*args, **kwargs)
        self.field.widget = SelectAndHiddenWidget()

    def js_initializer(self):
        return 'newRuleAdded'

    class Meta:
        icon = 'cog'


class AndOrBlock(blocks.ChoiceBlock):
    choices = [
        ('and', _('And')),
        ('or', _('Or'))
    ]

    class Meta:
        icon = 'plus'


class LogicBlock(blocks.StructBlock):
    rule_1 = RuleSelectBlock(required=True)
    operator = AndOrBlock(required=True)
    rule_2 = RuleSelectBlock(required=True)

    class Meta:
        icon = 'cogs'
        label = 'Nested Logic'
