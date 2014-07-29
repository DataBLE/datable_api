# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Mote.major'
        db.alter_column(u'motes_mote', 'major', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Mote.uuid'
        db.alter_column(u'motes_mote', 'uuid', self.gf('django.db.models.fields.CharField')(max_length=255))

        # Changing field 'Mote.minor'
        db.alter_column(u'motes_mote', 'minor', self.gf('django.db.models.fields.CharField')(max_length=255))

    def backwards(self, orm):

        # Changing field 'Mote.major'
        db.alter_column(u'motes_mote', 'major', self.gf('django.db.models.fields.CharField')(max_length=4))

        # Changing field 'Mote.uuid'
        db.alter_column(u'motes_mote', 'uuid', self.gf('django.db.models.fields.CharField')(max_length=32))

        # Changing field 'Mote.minor'
        db.alter_column(u'motes_mote', 'minor', self.gf('django.db.models.fields.CharField')(max_length=4))

    models = {
        u'motes.app': {
            'Meta': {'unique_together': "(('identifier', 'platform'),)", 'object_name': 'App'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'platform': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'motes.genderaction': {
            'Meta': {'object_name': 'GenderAction'},
            'action_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['motes.App']"}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mote': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['motes.Mote']"}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'motes.mote': {
            'Meta': {'unique_together': "(('uuid', 'major', 'minor'),)", 'object_name': 'Mote'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'major': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '255'}),
            'minor': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'3e2d21f625b449ad816ae0c33e5e5bed'", 'max_length': '255'})
        }
    }

    complete_apps = ['motes']