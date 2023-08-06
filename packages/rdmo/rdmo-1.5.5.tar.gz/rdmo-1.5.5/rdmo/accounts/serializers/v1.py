from django.conf import settings
from django.contrib.auth.models import Group, User
from django.contrib.sites.models import Site
from rest_framework import serializers

from rdmo.projects.models import Membership

from ..models import Role


class SiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Site
        fields = (
            'id',
            'name',
            'domain'
        )


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = (
            'id',
            'name'
        )


class RoleSerializer(serializers.ModelSerializer):

    member = SiteSerializer(many=True)
    manager = SiteSerializer(many=True)

    class Meta:
        model = Role
        fields = (
            'id',
            'member',
            'manager'
        )


class MembershipSerializer(serializers.ModelSerializer):

    class Meta:
        model = Membership
        fields = (
            'id',
            'project',
            'role'
        )


class UserSerializer(serializers.ModelSerializer):

    groups = GroupSerializer(many=True)
    role = RoleSerializer()
    memberships = MembershipSerializer(many=True)

    class Meta:
        model = User
        fields = [
            'id',
            'groups',
            'role',
            'memberships'
        ]
        if settings.USER_API:
            fields += [
                'username',
                'first_name',
                'last_name',
                'email'
            ]
