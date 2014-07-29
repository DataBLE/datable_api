# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Sighting'
        db.create_table(u'motes_sighting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mote', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motes.Mote'])),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motes.App'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'motes', ['Sighting'])


    def backwards(self, orm):
        # Deleting model 'Sighting'
        db.delete_table(u'motes_sighting')


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
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['motes.App']"}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mote': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['motes.Mote']"}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'motes.location': {
            'Meta': {'object_name': 'Location'},
            'address': ('django.db.models.fields.CharField', [], {'default': "'110 E 9th St'", 'max_length': '255'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "'Los Angeles'", 'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Default location'", 'max_length': '255'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {'default': "'POINT(-118.255389, 34.040589)'", 'null': 'True', 'blank': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'default': "'90031'", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'CA'", 'max_length': '255'})
        },
        u'motes.mote': {
            'Meta': {'unique_together': "(('uuid', 'major', 'minor'),)", 'object_name': 'Mote'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['motes.Location']"}),
            'major': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '255'}),
            'minor': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'repeat_interval': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'rssi': ('django.db.models.fields.FloatField', [], {'default': '-100'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'034f9892ebcd417a9f48f2aead8c4d8f'", 'max_length': '255'})
        },
        u'motes.sighting': {
            'Meta': {'object_name': 'Sighting'},
            'app': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['motes.App']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mote': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['motes.Mote']"})
        }
    }

    complete_apps = ['motes']