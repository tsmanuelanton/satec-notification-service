from django import forms

class RegisterForm(forms.Form):

    name = forms.CharField(max_length=32)
    lastname = forms.CharField(max_length=64)
    email = forms.EmailField(max_length=32)
    commercial_use = forms.ChoiceField(choices=[(True, "Sí"), (False, "No")], initial=(True, "Sí"), widget=forms.RadioSelect)
    company_name = forms.CharField(label="Nombre Organización", max_length=64, required=False)
    description = forms.CharField(widget=forms.Textarea, label="Descripción del uso", max_length=512)

    def clean_company_name(self):
        '''Valida que si el uso es comercial, se ingrese el nombre de la organización'''
        use = self.cleaned_data.get("commercial_use")
        company_name = self.cleaned_data.get("company_name")
        
        if use == "True" and not company_name:
            raise forms.ValidationError("Si el uso es comercial, debe ingresar el nombre de la organización")
        elif use == "False" and company_name:
            raise forms.ValidationError("Si el uso no es comercial, no debe ingresar el nombre de la organización")
        
        return company_name