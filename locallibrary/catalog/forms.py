from django import forms

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime  # Para revisar el rango de fechas de renovación.

class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text="Ingrese una fecha entre ahora y 4 semanas (por defecto 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        #  La fecha de verificación no está en el pasado.
        if data < datetime.date.today():
            raise ValidationError(_('Fecha inválida - renovación en pasado'))


        # La fecha de verificación está dentro del rango permitido por el bibliotecario (+4 semanas).
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Fecha inválida - renovación con más de 4 semanas de antelación'))

        #  Recuerda siempre devolver los datos limpiados.
        return data
