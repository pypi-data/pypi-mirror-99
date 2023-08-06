#   Copyright (c) 2020-2021 STiiiCK.
#
#   This source code is licensed under the GPLv3 license found in the
#   LICENSE file in the root directory of this source tree.

import uuid

from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL
Group = settings.GROUP_MODEL

#
# @author Omar Basem
#

class IdentityKey(models.Model):
    """
    A user has one IdentityKey created at registration time
    """
    public = models.CharField(max_length=44)
    deviceId = models.IntegerField(default=0)
    localId = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='identityKey')
    cipher = models.CharField(max_length=88)
    salt = models.CharField(max_length=44)


class SignedPreKey(models.Model):
    """
    A user has one SignedPreKey created at registration time
    """
    keyId = models.IntegerField()
    public = models.CharField(max_length=44)
    signature = models.CharField(max_length=88)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='signedPreKey')
    cipher = models.CharField(max_length=88)
    salt = models.CharField(max_length=44)
    active = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['keyId', 'user'], name='unique_signed_prekey')]


class PreKey(models.Model):
    """
    A user has a bunch of PreKeys created at registration time
    """
    keyId = models.IntegerField()
    public = models.CharField(max_length=44)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='preKeys')
    used = models.BooleanField(default=False)
    cipher = models.CharField(max_length=88)
    salt = models.CharField(max_length=44)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['keyId', 'user'], name='unique_prekey')]

    def __str__(self):
        return self.user.username + ' - ' + str(self.keyId) + ' - ' + str(self.id)

class EncryptingSenderKey(models.Model):
    """
    * Every member of a sticky session has a sender key. The sender key representation is broken down into two,
    'EncryptingSenderKey' (ESK) which only is owner should have, and a 'DecryptingSenderKey' (DSK) which is shared with other
    members of a sticky session individually. Those sender keys has a partyId and a chainId which together make the
    stickId (stickId = partyId || chainId).
    * These ESKs can also be used for a standard group session (not using sticky sessions).
    * The root key of an EncryptingSenderKey chain for a sticky session is called `StickyKey`.
    """
    keyId = models.IntegerField()
    preKey = models.OneToOneField(PreKey, on_delete=models.CASCADE, related_name='encryptingSenderKey')
    partyId = models.CharField(max_length=100)
    chainId = models.CharField(max_length=10)
    step = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='encryptingSenderKeys')
    chainKey = models.CharField(max_length=44)
    public = models.CharField(max_length=44)
    cipher = models.CharField(max_length=500)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['partyId', 'chainId', 'user'], name='unique_esk')]

    def __str__(self):
        return self.user.username + ': ' + self.partyId + '-' + self.chainId

class DecryptingSenderKey(models.Model):
    """
    * A user should get a DecryptingSenderKey (DSK) from every member of a sticky session to initialize the sticky session
    corresponding to that member and its stickId.
    * Note that the DecryptingSenderKey does not have a chainId field, unlike
    the EncryptingSenderKey, but it has a stickId field. The reason is that you would need to access the stickId more often
    on the DecryptingSenderKey, and you should not need to access the chainId directly. However, if you ever need to access
    the chainId you can simply do: `stickId[36:]`. This gets you whatever characters after the 36th character.
    The root key of a DecryptingSenderKey chain is called `StickyKey`.
    * A DecryptingSenderKey can be of a sticky session or a standard session. A sticky session DSK relates to users using
    the `ofUser` and `forUser` fields. A standard session DSK relates to users using the `ofOneTimeId` and `forOneTimeId`
    fields.
    """
    key = models.CharField(max_length=500)
    preKey = models.OneToOneField(PreKey, on_delete=models.CASCADE, related_name='decryptingSenderKey', blank=True, null=True)
    stickId = models.CharField(max_length=100)
    partyId = models.CharField(max_length=100, blank=True, null=True)
    ofUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='decryptingSenderKeys', null=True)
    forUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receivedSenderKeys', null=True)
    ofOneTimeId = models.CharField(max_length=100, blank=True, null=True)
    forOneTimeId = models.CharField(max_length=100, blank=True, null=True)




class Party(models.Model):
    """
    In the context of the Stick protocol, a "party" is one of three:
    1. A Group.
    2. A collection of groups and/or users
    3. My profile (currentUser profile - which includes of the currentUser's connections)

    Every user should be connected with a Party object created at registration time. Whenever a user shares
    with a collection of groups and/or users that does not correspond to any existing Party, a new Party object should
    be created. When sharing to a single group there is no need to create a party object (i.e.: using the groupId as the
    partyId would be sufficient).
    """
    id = models.CharField(primary_key=True, unique=True, max_length=1000)
    groups = models.ManyToManyField(Group, blank=True)
    connections = models.ManyToManyField(User, blank=True, related_name='party_connections')
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='party')

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid.uuid4()
        super(Party, self).save(*args, **kwargs)

