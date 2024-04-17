from djongo import models
from django.utils import timezone


# ТАСКА
class Task(models.Model):
    search_type = models.CharField(max_length=255, null=True, blank=True)
    search_name = models.CharField(max_length=255, null=True, blank=True)
    search_value = models.CharField(max_length=255)
    search_timestamp = models.CharField(max_length=255)
    status = models.CharField(max_length=255, null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)
    completed = models.DateTimeField(null=True, blank=True)
    celery_id = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return self.search_type, self.search_value


class MainInfo(models.Model):
    name = models.CharField(db_column='Name', max_length=20, verbose_name="Имя")
    surname = models.CharField(db_column='Surname', max_length=20, verbose_name="Фамилия")
    patronymic = models.CharField(db_column='Patronymic', max_length=20, verbose_name="Отчество")
    gender = models.CharField(db_column='Gender', max_length=20, verbose_name="Пол")
    date_of_birth = models.DateField(db_column='Date of birth', verbose_name="Дата рождения")
    place_of_birth = models.CharField(db_column='Place of birth', max_length=40, verbose_name="Место Рождения")
    residential_address = models.CharField(db_column='Residential address', max_length=40, verbose_name="Адрес прописки")
    religion = models.CharField(db_column='Religion', max_length=15, verbose_name="Религия")

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value

    class Meta:
        abstract = True
        verbose_name = 'Основная информация'

    @property
    def verbose_name(self):
        return self._meta.verbose_name


class Kindergarten(models.Model):
    name = models.CharField(db_column='Kindergarten name', max_length=30, verbose_name="Название сада")
    address = models.CharField(db_column='Kindergarten address', max_length=40, verbose_name="Адрес сада")

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value

    class Meta:
        abstract = True
        verbose_name = 'Информация о детских садах'

    @property
    def verbose_name(self):
        return self._meta.verbose_name

    def __str__(self):
        return self.name


class School(models.Model):
    name = models.CharField(db_column='School name', max_length=30, verbose_name="Название школы")
    address = models.CharField(db_column='School address', max_length=40, verbose_name="Адрес школы")

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value

    class Meta:
        abstract = True
        verbose_name = 'Информация о школах'

    @property
    def verbose_name(self):
        return self._meta.verbose_name

    def __str__(self):
        return self.name


class College(models.Model):
    name = models.CharField(db_column='College name', max_length=30, verbose_name="Название колледжа")
    address = models.CharField(db_column='College address', max_length=40, verbose_name="Адрес колледжа")

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value

    class Meta:
        abstract = True
        verbose_name = 'Информация о колледжах'

    @property
    def verbose_name(self):
        return self._meta.verbose_name

    def __str__(self):
        return self.name


class University(models.Model):
    name = models.CharField(db_column='University name', max_length=30, verbose_name="Название университета")
    address = models.CharField(db_column='University address', max_length=40, verbose_name="Адрес университета")

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value

    class Meta:
        abstract = True
        verbose_name = 'Информация об университете'

    @property
    def verbose_name(self):
        return self._meta.verbose_name

    def __str__(self):
        return self.name


class Work(models.Model):
    name = models.CharField(db_column='Company name', max_length=30, verbose_name="Название работы")
    address = models.CharField(db_column='Work address', max_length=40, verbose_name="Адрес работы")
    position = models.CharField(db_column='Person position', max_length=20, verbose_name="Должность")
    work_number = models.CharField(db_column='Work number', max_length=20, verbose_name="Рабочий номер")

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value

    class Meta:
        abstract = True
        verbose_name = 'Информация о работе'

    @property
    def verbose_name(self):
        return self._meta.verbose_name


class Interest(models.Model):
    name = models.CharField(db_column='Interest name', max_length=30, verbose_name="Название хобби")

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value

    class Meta:
        abstract = True
        verbose_name = 'Информация о хобби'

    @property
    def verbose_name(self):
        return self._meta.verbose_name

    def __str__(self):
        return self.name


class Income(models.Model):
    name = models.CharField(db_column='Income name', max_length=30, verbose_name="Название дохода")
    author = models.CharField(db_column='Income from', max_length=30, verbose_name="От чего")
    amount = models.CharField(db_column='Amount', max_length=20, verbose_name="Сумма")
    comment = models.TextField(db_column='Income comment', verbose_name="Комментарий")

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value

    class Meta:
        abstract = True
        verbose_name = 'Информация о доходах'

    @property
    def verbose_name(self):
        return self._meta.verbose_name


class Expenses(models.Model):
    name = models.CharField(db_column='Expenses name', max_length=30, verbose_name="Название расхода")
    receiver = models.CharField(db_column='Expenses to', max_length=30, verbose_name="На что")
    amount = models.CharField(db_column='Amount', max_length=20, verbose_name="Сумма")
    comment = models.TextField(db_column='Expenses comment', verbose_name="Комментарий")

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value

    class Meta:
        abstract = True
        verbose_name = 'Информация о расходах'

    @property
    def verbose_name(self):
        return self._meta.verbose_name


class BankAccount(models.Model):
    name = models.CharField(db_column='Bank name', max_length=30, verbose_name="Название банка")
    number = models.CharField(db_column='Account number', max_length=40, verbose_name="Имя кошелька")
    address = models.CharField(db_column='Bank address', max_length=20, verbose_name="Адрес банка")
    comment = models.TextField(db_column='Account comment', verbose_name="Комментаий")

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value

    class Meta:
        abstract = True
        verbose_name = 'Информация о банковских счетах'

    @property
    def verbose_name(self):
        return self._meta.verbose_name


class ElectronicWallet(models.Model):
    name = models.CharField(db_column='Wallet name', max_length=30, verbose_name="Название кошелька")
    number = models.CharField(db_column='Wallet number', max_length=40, verbose_name="Номер кошелька")
    account_type = models.CharField(db_column='Account type', max_length=20, verbose_name="Тип кошелька")
    comment = models.TextField(db_column='Account comment', verbose_name="Комментарий")

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value

    class Meta:
        abstract = True
        verbose_name = 'Информация о электронных счетах'

    @property
    def verbose_name(self):
        return self._meta.verbose_name


class Estate(models.Model):
    name = models.CharField(db_column='Estate name', max_length=30, verbose_name="Вид собственности")
    estate_type = models.CharField(db_column='Estate type', max_length=20, verbose_name="Тип собственности")
    comment = models.TextField(db_column='Estate comment', verbose_name="Комментарий")

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value

    class Meta:
        abstract = True
        verbose_name = 'Информация о собственности'

    @property
    def verbose_name(self):
        return self._meta.verbose_name


class SocialNetwork(models.Model):
    name = models.CharField(db_column='Network name', max_length=30, verbose_name="Название социальной сети")
    account_type = models.CharField(db_column='Account type', max_length=20, verbose_name="Тип аккаунта")
    account_id = models.CharField(db_column='Account id', max_length=30, verbose_name="ID аккаунта")
    account_login = models.CharField(db_column='Account login', max_length=30, verbose_name="Логин аккаунта")
    account_email = models.EmailField(db_column='Email', verbose_name="Email аккаунта")
    account_password = models.CharField(db_column='Account password', max_length=30, verbose_name="Пароль аккаунта")
    comment = models.TextField(db_column='Account comment', verbose_name="Комментарий")

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value

    class Meta:
        abstract = True
        verbose_name = 'Информация о социальных сетях'

    @property
    def verbose_name(self):
        return self._meta.verbose_name


class Messenger(models.Model):
    name = models.CharField(db_column='Messenger name', max_length=30, verbose_name="Название мессенджера")
    account_type = models.CharField(db_column='Account type', max_length=20, verbose_name="Тип аккаунта")
    account_login = models.CharField(db_column='Account login', max_length=30, verbose_name="Логин аккаунта")
    account_phone = models.CharField(db_column='Phone number', max_length=15, verbose_name="Телефонный номер аккаунта")
    account_password = models.CharField(db_column='Account password', max_length=30, verbose_name="Пароль аккаунта")
    comment = models.TextField(db_column='Account comment', verbose_name="Комментарий")

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value

    class Meta:
        abstract = True
        verbose_name = 'Информация о мессенджерах'

    @property
    def verbose_name(self):
        return self._meta.verbose_name


class Email(models.Model):
    name = models.CharField(db_column='Email name', max_length=30, verbose_name="Имя почтового ящика")
    account_login = models.CharField(db_column='Account login', max_length=30, verbose_name="Тип аккаунта")
    account_password = models.CharField(db_column='Account password', max_length=30, verbose_name="Пароль аккаунта")
    comment = models.TextField(db_column='Account comment', verbose_name="Комментарий")

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value

    class Meta:
        abstract = True
        verbose_name = 'Информация о почтовых ящиках'

    @property
    def verbose_name(self):
        return self._meta.verbose_name


class GamePlatform(models.Model):
    name = models.CharField(db_column='Platform name', max_length=30, verbose_name="Название платформы")
    account_type = models.CharField(db_column='Account type', max_length=20, verbose_name="Тип аккаунта")
    account_id = models.CharField(db_column='Account id', max_length=30, verbose_name="ID аккаунта")
    account_login = models.CharField(db_column='Account login', max_length=30, verbose_name="Логин аккаунта")
    account_email = models.EmailField(db_column='Email', verbose_name="Email аккаунта")
    account_password = models.CharField(db_column='Account password', max_length=30, verbose_name="Пароль аккаунта")
    comment = models.TextField(db_column='Account comment', verbose_name="Комментарий")

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value

    class Meta:
        abstract = True
        verbose_name = 'Информация о игровых платформах'

    @property
    def verbose_name(self):
        return self._meta.verbose_name


class Forum(models.Model):
    name = models.CharField(db_column='Forum name', max_length=30, verbose_name="Название форума")
    account_type = models.CharField(db_column='Account type', max_length=20, verbose_name="Тип аккаунта")
    account_id = models.CharField(db_column='Account id', max_length=30, verbose_name="ID аккаунта")
    account_login = models.CharField(db_column='Account login', max_length=30, verbose_name="Логин аккаунта")
    account_email = models.EmailField(db_column='Email', verbose_name="Email аккаунта")
    account_password = models.CharField(db_column='Account password', max_length=30, verbose_name="Пароль аккаунта")
    comment = models.TextField(db_column='Account comment', verbose_name="Комментарий")

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value

    class Meta:
        abstract = True
        verbose_name = 'Информация о форумах'

    @property
    def verbose_name(self):
        return self._meta.verbose_name


class MAC(models.Model):
    name = models.CharField(db_column='Device type', max_length=30, verbose_name="Тип устройства")
    firm = models.CharField(db_column='Device firm', max_length=20, verbose_name="Фирма устройства")
    model = models.CharField(db_column='Device model', max_length=50, verbose_name="Модель устройства")
    mac = models.CharField(db_column='MAC id', max_length=30, verbose_name="МАС")
    comment = models.TextField(db_column='MAC comment', verbose_name="Комментарий")

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value

    class Meta:
        abstract = True
        verbose_name = 'Информация о МАКе'

    @property
    def verbose_name(self):
        return self._meta.verbose_name

    def __str__(self):
        return self.mac


class IP (models.Model):
    name = models.CharField(db_column='Device type', max_length=30, verbose_name="Тип устройства")
    firm = models.CharField(db_column='Device firm', max_length=20, verbose_name="Фирма устройства")
    model = models.CharField(db_column='Device model', max_length=50, verbose_name="Модель устройства")
    ip = models.CharField(db_column='IP id', max_length=30, verbose_name="IP")
    comment = models.TextField(db_column='IP comment', verbose_name="Комментарий")

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value

    class Meta:
        abstract = True
        verbose_name = 'Информация о IP'

    @property
    def verbose_name(self):
        return self._meta.verbose_name

    def __str__(self):
        return self.ip


class HWID(models.Model):
    name = models.CharField(db_column='Device type', max_length=30, verbose_name="Тип устройства")
    firm = models.CharField(db_column='Device firm', max_length=20, verbose_name="Фирма устройтсва")
    model = models.CharField(db_column='Device model', max_length=50, verbose_name="Модель устройтсва")
    hwid = models.CharField(db_column='HWID id', max_length=30, verbose_name="HWID")
    comment = models.TextField(db_column='HWID comment', verbose_name="Комментарий")

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value

    class Meta:
        abstract = True
        verbose_name = 'Информация о HWID'

    @property
    def verbose_name(self):
        return self._meta.verbose_name

    def __str__(self):
        return self.hwid


class DNS(models.Model):
    name = models.CharField(db_column='Device type', max_length=30, verbose_name="Тип устройтсва")
    firm = models.CharField(db_column='Device firm', max_length=20, verbose_name="Фирма устройтсва")
    model = models.CharField(db_column='Device model', max_length=50, verbose_name="Модель устройтсва")
    dns = models.CharField(db_column='DNS id', max_length=30, verbose_name="DNS")
    comment = models.TextField(db_column='DNS comment', verbose_name="Комментарий")

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value

    class Meta:
        abstract = True
        verbose_name = 'Информация о DNS'

    @property
    def verbose_name(self):
        return self._meta.verbose_name

    def __str__(self):
        return self.dns


class GeoTags(models.Model):
    name = models.CharField(db_column='Tag name', max_length=30, verbose_name="Название метки")
    coordinates = models.CharField(db_column='Coordinates', max_length=200, verbose_name="Координаты")
    type = models.CharField(db_column='Tag type', max_length=50, verbose_name="Тип метки")
    comment = models.TextField(db_column='Tag comment', verbose_name="Комметарий")

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value

    class Meta:
        abstract = True
        verbose_name = 'Информация о геометках'

    @property
    def verbose_name(self):
        return self._meta.verbose_name


class Phone(models.Model):
    phone_type = models.CharField(db_column='Phone type', max_length=30, verbose_name="Тип номера")
    model = models.CharField(db_column='Device model', max_length=50, verbose_name="Модель телефона")
    IMEI = models.CharField(db_column='Phone IMEI', max_length=30, verbose_name="IMEI")
    number = models.CharField(db_column='Phone number', max_length=10, verbose_name="Номер телефона")
    sim_card = models.CharField(db_column='SimCard number', max_length=30, verbose_name="Номер симкарты")
    comment = models.TextField(db_column='Phone comment', verbose_name="Комментарий")

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value

    class Meta:
        abstract = True
        verbose_name = 'Информация о телефонах'

    @property
    def verbose_name(self):
        return self._meta.verbose_name


class Passport(models.Model):
    serial = models.CharField(db_column='Passport serial', max_length=10, verbose_name="Серия паспорта")
    number = models.CharField(db_column='Passport number', max_length=10, verbose_name="Номер паспорта")
    departament = models.CharField(db_column='Departament', max_length=50, verbose_name="Поздразделение выдавшее")
    departament_number = models.CharField(db_column='Departament number', max_length=15, verbose_name="Номер подразделения")
    issue_date = models.DateField(db_column='Passport issue date', verbose_name="Дата выдачи")

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value

    class Meta:
        abstract = True
        verbose_name = 'Информация о паспортах'

    @property
    def verbose_name(self):
        return self._meta.verbose_name


class InternationalPassport(models.Model):
    serial = models.CharField(db_column='International passport serial', max_length=10, verbose_name="Серия паспорта")
    number = models.CharField(db_column='International passport number', max_length=10, verbose_name="Номер паспорта")
    departament = models.CharField(db_column='Departament', max_length=50, verbose_name="Подразделение выдавшее")
    departament_number = models.CharField(db_column='Departament number', max_length=15, verbose_name="Номер подразделения")
    issue_date = models.DateField(db_column='International passport issue date', verbose_name="Дата выдачи")

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value

    class Meta:
        abstract = True
        verbose_name = 'Информация о загран паспортах'

    @property
    def verbose_name(self):
        return self._meta.verbose_name


class DriverLicense(models.Model):
    number = models.CharField(db_column='Driver license number', max_length=10, verbose_name="Номер прав")
    departament = models.CharField(db_column='Departament', max_length=50, verbose_name="Подразделение выдавшее")
    categories = models.CharField(db_column='Categories', max_length=15, verbose_name="Категории прав")
    issue_date = models.DateField(db_column='International passport issue date', verbose_name="Дата выдачи")

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value

    class Meta:
        abstract = True
        verbose_name = 'Информация о правах'

    @property
    def verbose_name(self):
        return self._meta.verbose_name


class InsuranceCertificate(models.Model):
    number = models.CharField(db_column='Insurance certificate number', max_length=10, verbose_name="Номер страховки")
    issue_date = models.DateField(db_column='Insurance certificate issue date', verbose_name="Дата оформления")

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value

    class Meta:
        abstract = True
        verbose_name = 'Информация о страховке'

    @property
    def verbose_name(self):
        return self._meta.verbose_name


class Policy(models.Model):
    serial = models.CharField(db_column='Policy serial', max_length=10, verbose_name="Серия полиса")
    number = models.CharField(db_column='Policy number', max_length=10, verbose_name="Номер полиса")
    departament = models.CharField(db_column='Departament', max_length=50, verbose_name="Подразделение выдавшее")
    issue_date = models.DateField(db_column='Policy issue date', verbose_name="Дата выдачи")

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value

    class Meta:
        abstract = True
        verbose_name = 'Информация о полисе'

    @property
    def verbose_name(self):
        return self._meta.verbose_name


class BirthCertificate(models.Model):
    number = models.CharField(db_column='Birth certificate number', max_length=10, verbose_name="Номер свидетельства")
    departament = models.CharField(db_column='Departament', max_length=50, verbose_name="Подразделение выдавшее")
    act_number = models.CharField(db_column='Act number', max_length=10, verbose_name="Номер акта")
    issue_date = models.DateField(db_column='Birth certificate issue date', verbose_name="Дата выдачи")

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value

    class Meta:
        abstract = True
        verbose_name = 'Информация о свидетельстве о рождении'

    @property
    def verbose_name(self):
        return self._meta.verbose_name


class MilitaryID(models.Model):
    number = models.CharField(db_column='Military ID number', max_length=10, verbose_name="Номер билета")
    departament = models.CharField(db_column='Departament', max_length=50, verbose_name="Подразделение выдавшее")
    issue_date = models.DateField(db_column='Military ID issue date', verbose_name="Дата выдачи")

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value

    class Meta:
        abstract = True
        verbose_name = 'Информация о военном билете'

    @property
    def verbose_name(self):
        return self._meta.verbose_name


class EmploymentHistory(models.Model):
    number = models.CharField(db_column='Employment history number', max_length=10, verbose_name="Номер книги")
    departament = models.CharField(db_column='Departament', max_length=50, verbose_name="Подразделение выдавшее")
    issue_date = models.DateField(db_column='Employment history issue date', verbose_name="Дата выдачи")

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value

    class Meta:
        abstract = True
        verbose_name = 'Информация о трудовой книге'

    @property
    def verbose_name(self):
        return self._meta.verbose_name


class EducationDocument(models.Model):
    number = models.CharField(db_column='Education document number', max_length=10, verbose_name="Номер удостоверения")
    departament = models.CharField(db_column='Departament', max_length=50, verbose_name="Подразделение выдавшее")
    issue_date = models.DateField(db_column='Education document issue date', verbose_name="Дата выдачи")

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value

    class Meta:
        abstract = True
        verbose_name = 'Информация о документе об образовании'

    @property
    def verbose_name(self):
        return self._meta.verbose_name


class Document(models.Model):
    passports = models.ArrayModelField(model_container=Passport, )
    international_passports = models.ArrayModelField(model_container=InternationalPassport, )
    driver_licenses = models.ArrayModelField(model_container=DriverLicense, )
    insurance_certificate = models.EmbeddedModelField(model_container=InsuranceCertificate, )
    policy = models.EmbeddedModelField(model_container=Policy, )
    birth_certificate = models.EmbeddedModelField(model_container=BirthCertificate, )
    military_id = models.EmbeddedModelField(model_container=MilitaryID, )
    employment_history = models.EmbeddedModelField(model_container=EmploymentHistory, )
    education_documents = models.ArrayModelField(model_container=EducationDocument, )
    itn = models.CharField(db_column='ITN', max_length=20)


class Person(models.Model):
    # _id = models.ObjectIdField()
    main_info = models.EmbeddedModelField(model_container=MainInfo, )
    kindergartens = models.ArrayModelField(model_container=Kindergarten, )
    schools = models.ArrayModelField(model_container=School, )
    colleges = models.ArrayModelField(model_container=College, )
    universities = models.ArrayModelField(model_container=University, )
    works = models.ArrayModelField(model_container=Work, )
    interests = models.ArrayModelField(model_container=Interest, )
    incomes = models.ArrayModelField(model_container=Income, )
    expenses = models.ArrayModelField(model_container=Expenses, )
    bank_accounts = models.ArrayModelField(model_container=BankAccount, )
    electronic_wallets = models.ArrayModelField(model_container=ElectronicWallet, )
    estate = models.ArrayModelField(model_container=Estate, )
    social_networks = models.ArrayModelField(model_container=SocialNetwork, )
    messengers = models.ArrayModelField(model_container=Messenger, )
    emails = models.ArrayModelField(model_container=Email, )
    game_platforms = models.ArrayModelField(model_container=GamePlatform, )
    forums = models.ArrayModelField(model_container=Forum, )
    MAC_addresses = models.ArrayModelField(model_container=MAC, )
    IP_addresses = models.ArrayModelField(model_container=IP, )
    HWIDs = models.ArrayModelField(model_container=HWID, )
    DNSs = models.ArrayModelField(model_container=DNS, )
    geo_tags = models.ArrayModelField(model_container=GeoTags, )
    phones = models.ArrayModelField(model_container=Phone, )
    documents = models.ArrayReferenceField(to=Document, on_delete=models.CASCADE)

    def attrs(self):
        for attr, value in self.__dict__.items():
            if attr != '_state':
                yield attr, value
    @property
    def person_id(self):
        return self._id
