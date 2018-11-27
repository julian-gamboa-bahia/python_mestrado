# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import micro.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Laminas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('NOME', models.CharField(max_length=100, verbose_name='<i>Nome</i>')),
                ('DENSIDADE', models.FloatField(verbose_name='<i>Densidade</i> [kg/m\xb3]', validators=[micro.models.validate_not_neg_zero])),
                ('E1', models.FloatField(blank=True, help_text='M\xf3dulo de elasticidade longitudinal', null=True, verbose_name='<i>\u0395</i>\xa0\xa0<sub>1</sub> [Pa]', validators=[micro.models.validate_not_negative])),
                ('E2', models.FloatField(blank=True, help_text='M\xf3dulo de elasticidade transversal', null=True, verbose_name='<i>\u0395</i>\xa0\xa0<sub>2</sub> [Pa]', validators=[micro.models.validate_not_negative])),
                ('E3', models.FloatField(blank=True, help_text='M\xf3dulo de elasticidade interlaminar', null=True, verbose_name='<i>\u0395</i>\xa0\xa0<sub>3</sub> [Pa]', validators=[micro.models.validate_not_negative])),
                ('G12', models.FloatField(blank=True, help_text='M\xf3dulo de cisalhamento no plano', null=True, verbose_name='<i>G</i>\xa0\xa0<sub>12</sub> [Pa]', validators=[micro.models.validate_not_negative])),
                ('G13', models.FloatField(blank=True, help_text='M\xf3dulo de cisalhamento interlaminar longitudinal', null=True, verbose_name='<i>G</i>\xa0\xa0<sub>13</sub> [Pa]', validators=[micro.models.validate_not_negative])),
                ('G23', models.FloatField(blank=True, help_text='M\xf3dulo de cisalhamento interlaminar transversal', null=True, verbose_name='<i>G</i>\xa0\xa0<sub>23</sub> [Pa]', validators=[micro.models.validate_not_negative])),
                ('NU12', models.FloatField(blank=True, help_text='Coeficiente de Poisson no plano', null=True, verbose_name='<i>\u03bd</i>\xa0\xa0<sub>12</sub>', validators=[micro.models.validate_not_negative])),
                ('NU13', models.FloatField(blank=True, help_text='Coeficiente de Poisson interlaminar longitudinal', null=True, verbose_name='<i>\u03bd</i>\xa0\xa0<sub>13</sub>', validators=[micro.models.validate_not_negative])),
                ('NU23', models.FloatField(blank=True, help_text='Coeficiente de Poisson interlaminar transversal', null=True, verbose_name='<i>\u03bd</i>\xa0\xa0<sub>23</sub>', validators=[micro.models.validate_not_negative])),
                ('SIGMA_T_1', models.FloatField(blank=True, help_text='Resist\xeancia \xe0 tra\xe7\xe3o longitudinal', null=True, verbose_name='<i>\u03c3</i><i><sup>T</sup></i>\xa0\xa0<sub>1</sub> [Pa]', validators=[micro.models.validate_not_negative])),
                ('SIGMA_T_2', models.FloatField(blank=True, help_text='Resist\xeancia \xe0 tra\xe7\xe3o transversal', null=True, verbose_name='<i>\u03c3</i><i><sup>T</sup></i>\xa0\xa0<sub>2</sub> [Pa]', validators=[micro.models.validate_not_negative])),
                ('SIGMA_C_1', models.FloatField(blank=True, help_text='Resist\xeancia \xe0 compress\xe3o longitudinal', null=True, verbose_name='<i>\u03c3</i><i><sup>C</sup></i>\xa0\xa0<sub>1</sub> [Pa]', validators=[micro.models.validate_not_negative])),
                ('SIGMA_C_2', models.FloatField(blank=True, help_text='Resist\xeancia \xe0 compress\xe3o transversal', null=True, verbose_name='<i>\u03c3</i><i><sup>C</sup></i>\xa0\xa0<sub>2</sub> [Pa]', validators=[micro.models.validate_not_negative])),
                ('TAU12', models.FloatField(blank=True, help_text='Resist\xeancia ao cisalhamento no plano', null=True, verbose_name='<i>\u03c4</i>\xa0\xa0<sub>12</sub> [Pa]', validators=[micro.models.validate_not_negative])),
                ('TAU13', models.FloatField(blank=True, help_text='Resist\xeancia ao cisalhamento interlaminar longitudinal', null=True, verbose_name='<i>\u03c4</i>\xa0\xa0<sub>13</sub> [Pa]', validators=[micro.models.validate_not_negative])),
                ('TAU23', models.FloatField(blank=True, help_text='Resist\xeancia ao cisalhamento interlaminar transversal', null=True, verbose_name='<i>\u03c4</i>\xa0\xa0<sub>23</sub> [Pa]', validators=[micro.models.validate_not_negative])),
                ('EPSILON_T_1', models.FloatField(blank=True, help_text='Deforma\xe7\xe3o de tra\xe7\xe3o longitudinal', null=True, verbose_name='<i>\u03b5</i><i><sup>T</sup></i>\xa0\xa0<sub>1</sub> [%]', validators=[micro.models.validate_not_negative])),
                ('EPSILON_T_2', models.FloatField(blank=True, help_text='Deforma\xe7\xe3o de tra\xe7\xe3o transversal', null=True, verbose_name='<i>\u03b5</i><i><sup>T</sup></i>\xa0\xa0<sub>2</sub> [%]', validators=[micro.models.validate_not_negative])),
                ('EPSILON_C_1', models.FloatField(blank=True, help_text='Deforma\xe7\xe3o de compress\xe3o transversal', null=True, verbose_name='<i>\u03b5</i><i><sup>C</sup></i>\xa0\xa0<sub>1</sub> [%]', validators=[micro.models.validate_not_negative])),
                ('EPSILON_C_2', models.FloatField(blank=True, help_text='Deforma\xe7\xe3o de compress\xe3o transversal', null=True, verbose_name='<i>\u03b5</i><i><sup>C</sup></i>\xa0\xa0<sub>2</sub> [%]', validators=[micro.models.validate_not_negative])),
                ('GAMMA12', models.FloatField(blank=True, help_text='Deforma\xe7\xe3o Cisalhiante', null=True, verbose_name='<i>\u03b3</i>\xa0\xa0<sub>12</sub>', validators=[micro.models.validate_not_negative])),
                ('ALPHA1', models.FloatField(help_text='Coeficiente de expans\xe3o t\xe9rmica longitudinal', null=True, verbose_name='<i>\u03b1</i>\xa0\xa0<sub>1</sub> [m/m/\xb0C]', blank=True)),
                ('ALPHA2', models.FloatField(help_text='Coeficiente de expans\xe3o t\xe9rmica transversal', null=True, verbose_name='<i>\u03b1</i>\xa0\xa0<sub>2</sub> [m/m/\xb0C]', blank=True)),
                ('ALPHA3', models.FloatField(help_text='Coeficiente de expans\xe3o t\xe9rmica interlaminar', null=True, verbose_name='<i>\u03b1</i>\xa0\xa0<sub>3</sub> [m/m/\xb0C]', blank=True)),
                ('BETA1', models.FloatField(blank=True, help_text='Coeficiente de expans\xe3o higrosc\xf3pica longitudinal', null=True, verbose_name='<i>\u03b2</i>\xa0\xa0<sub>1</sub> [m/m/%m]', validators=[micro.models.validate_not_negative])),
                ('BETA2', models.FloatField(blank=True, help_text='Coeficiente de expans\xe3o higrosc\xf3pica transversal', null=True, verbose_name='<i>\u03b2</i>\xa0\xa0<sub>2</sub> [m/m/%m]', validators=[micro.models.validate_not_negative])),
                ('BETA3', models.FloatField(blank=True, help_text='Coeficiente de expans\xe3o higrosc\xf3pica interlaminar', null=True, verbose_name='<i>\u03b2</i>\xa0\xa0<sub>3</sub> [m/m/%m]', validators=[micro.models.validate_not_negative])),
                ('C', models.FloatField(blank=True, help_text='Calor Espec\xedfico', null=True, verbose_name='<i>c</i> [J/kg/K]', validators=[micro.models.validate_not_negative])),
                ('K1', models.FloatField(blank=True, help_text='Condutividade t\xe9rmica longitudinal', null=True, verbose_name='<i>K</i>\xa0\xa0<sub>1</sub> [W/m/K]', validators=[micro.models.validate_not_negative])),
                ('K2', models.FloatField(blank=True, help_text='Condutividade t\xe9rmica transversal', null=True, verbose_name='<i>K</i>\xa0\xa0<sub>2</sub> [W/m/K]', validators=[micro.models.validate_not_negative])),
                ('K3', models.FloatField(blank=True, help_text='Condutividade t\xe9rmica interlaminar', null=True, verbose_name='<i>K</i>\xa0\xa0<sub>3</sub> [W/m/K]', validators=[micro.models.validate_not_negative])),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
        ),
    ]
