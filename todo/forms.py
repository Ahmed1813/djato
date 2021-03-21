from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Submit, HTML, Field
from django import forms

from .models import GroupModel, TodosModel


class GroupModelForm(forms.ModelForm):

    class Meta:
        model = GroupModel
        fields = ("group_name", "group_description")
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['group_name'].label = "Group Title"
        self.fields['group_description'].label = "Group Description"
        self.fields['group_description'].widget = forms.Textarea(attrs={"rows": 5})
        self.fields['group_description'].required = True


        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            'group_name',
            "group_description",
            HTML('<a class="btn btn-danger" href="{% url \'todo:groups\' %}"><i class="fa fa-md fa-times"></i> <span>Cancel</span></a>'),
            HTML('<button type="submit" class="btn btn-primary float-right"><i class="fa fa-md {{ submit_icon }}"></i> <span>{{ submit_value }}</span></a>'),
        )


class TodosModelForm(forms.ModelForm):

    class Meta:
        model = TodosModel
        fields = ("title", "description", "completed")
    

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = "Todo Name"
        self.fields['description'].label = "Todo Description"
        self.fields['description'].widget = forms.Textarea(attrs={"rows": 5})
        self.fields['description'].required = True


        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            'title',
            "description",
            "completed",
            HTML('<a class="btn btn-danger" href="{% url \'todo:todos_list\' group_id %}"><i class="fa fa-md fa-times"></i> <span>Cancel</span></a>'),
            HTML('<button type="submit" class="btn btn-primary float-right"><i class="fa fa-md {{ submit_icon }}"></i> <span>{{ submit_value }}</span></a>'),
        )


