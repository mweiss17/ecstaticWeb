# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Events.role6'
        db.delete_column(u'sds_events', 'role6')

        # Deleting field 'Events.organizer6'
        db.delete_column(u'sds_events', 'organizer6_id')

        # Deleting field 'Events.organizer5'
        db.delete_column(u'sds_events', 'organizer5_id')

        # Deleting field 'Events.role4'
        db.delete_column(u'sds_events', 'role4')

        # Deleting field 'Events.organizer4'
        db.delete_column(u'sds_events', 'organizer4_id')

        # Deleting field 'Events.role5'
        db.delete_column(u'sds_events', 'role5')


        # Changing field 'Events.role3'
        db.alter_column(u'sds_events', 'role3', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'Events.role2'
        db.alter_column(u'sds_events', 'role2', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

    def backwards(self, orm):
        # Adding field 'Events.role6'
        db.add_column(u'sds_events', 'role6',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Events.organizer6'
        db.add_column(u'sds_events', 'organizer6',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='organizerProfile6', null=True, to=orm['sds.UserProfile'], blank=True),
                      keep_default=False)

        # Adding field 'Events.organizer5'
        db.add_column(u'sds_events', 'organizer5',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='organizerProfile5', null=True, to=orm['sds.UserProfile'], blank=True),
                      keep_default=False)

        # Adding field 'Events.role4'
        db.add_column(u'sds_events', 'role4',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'Events.organizer4'
        db.add_column(u'sds_events', 'organizer4',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='organizerProfile4', null=True, to=orm['sds.UserProfile'], blank=True),
                      keep_default=False)

        # Adding field 'Events.role5'
        db.add_column(u'sds_events', 'role5',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)


        # Changing field 'Events.role3'
        db.alter_column(u'sds_events', 'role3', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

        # Changing field 'Events.role2'
        db.alter_column(u'sds_events', 'role2', self.gf('django.db.models.fields.CharField')(default='', max_length=255))

    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sds.events': {
            'Meta': {'object_name': 'Events'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'eventPic': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sds.Photos']", 'unique': 'True'}),
            'google_map_link': ('django.db.models.fields.CharField', [], {'max_length': '1000'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'organizer1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'organizerProfile1'", 'null': 'True', 'to': u"orm['sds.UserProfile']"}),
            'organizer2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'organizerProfile2'", 'null': 'True', 'to': u"orm['sds.UserProfile']"}),
            'organizer3': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'organizerProfile3'", 'null': 'True', 'to': u"orm['sds.UserProfile']"}),
            'role1': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'role2': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'role3': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sds.music': {
            'Meta': {'object_name': 'Music'},
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intention': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'songname': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uploadedSong': ('django.db.models.fields.files.FileField', [], {'default': "'uploadedSongs'", 'max_length': '100'})
        },
        u'sds.photos': {
            'Meta': {'object_name': 'Photos'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'photoFile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'photographer': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'pictureType': ('django.db.models.fields.CharField', [], {'default': "'pp'", 'max_length': '2'})
        },
        u'sds.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profilePic': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sds.Photos']"}),
            'signupDate': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['sds']