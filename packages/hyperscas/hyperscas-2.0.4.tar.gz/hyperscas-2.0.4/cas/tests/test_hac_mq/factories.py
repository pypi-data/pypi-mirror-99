import factory


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'test_hac_mq.User'


class UserGroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'test_hac_mq.UserGroup'


class DomainFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'cas.Domain'

    host = 'https://dmp.hypers.com.cn'
