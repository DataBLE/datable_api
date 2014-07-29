# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Mote'
        db.create_table(u'motes_mote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('uuid', self.gf('django.db.models.fields.CharField')(default='8d21f3c8796449668c41db8c2c1378a0', max_length=32)),
            ('major', self.gf('django.db.models.fields.CharField')(default=0, max_length=4)),
            ('minor', self.gf('django.db.models.fields.CharField')(default=0, max_length=4)),
        ))
        db.send_create_signal(u'motes', ['Mote'])

        # Adding unique constraint on 'Mote', fields ['uuid', 'major', 'minor']
        db.create_unique(u'motes_mote', ['uuid', 'major', 'minor'])

        # Adding model 'App'
        db.create_table(u'motes_app', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('platform', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'motes', ['App'])

        # Adding unique constraint on 'App', fields ['identifier', 'platform']
        db.create_unique(u'motes_app', ['identifier', 'platform'])

        # Adding model 'GenderAction'
        db.create_table(u'motes_genderaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mote', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motes.Mote'])),
            ('app', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['motes.App'])),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('action_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'motes', ['GenderAction'])


    def backwards(self, orm):
        # Removing unique constraint on 'App', fields ['identifier', 'platform']
        db.delete_unique(u'motes_app', ['identifier', 'platform'])

        # Removing unique constraint on 'Mote', fields ['uuid', 'major', 'minor']
        db.delete_unique(u'motes_mote', ['uuid', 'major', 'minor'])

        # Deleting model 'Mote'
        db.delete_table(u'motes_mote')

        # Deleting model 'App'
        db.delete_table(u'motes_app')

        # Deleting model 'GenderAction'
        db.delete_table(u'motes_genderaction')


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
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'motes.mote': {
            'Meta': {'unique_together': "(('uuid', 'major', 'minor'),)", 'object_name': 'Mote'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'major': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '4'}),
            'minor': ('django.db.models.fields.CharField', [], {'default': '0', 'max_length': '4'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uuid': ('django.db.models.fields.CharField', [], {'default': "'d1285d20dc1b4171be4313793dbd3c21'", 'max_length': '32'})
        }
    }

    complete_apps = ['motes']