# -*- coding: utf-8 -*-

from copy import deepcopy
from DateTime import DateTime
from Products.MeetingCommunes.config import FINANCE_ADVICES_COLLECTION_ID
from Products.PloneMeeting.profiles import AnnexTypeDescriptor
from Products.PloneMeeting.profiles import CategoryDescriptor
from Products.PloneMeeting.profiles import ItemAnnexTypeDescriptor
from Products.PloneMeeting.profiles import ItemTemplateDescriptor
from Products.PloneMeeting.profiles import MeetingConfigDescriptor
from Products.PloneMeeting.profiles import OrgDescriptor
from Products.PloneMeeting.profiles import PloneMeetingConfiguration
from Products.PloneMeeting.profiles import PodTemplateDescriptor
from Products.PloneMeeting.profiles import RecurringItemDescriptor
from Products.PloneMeeting.profiles import StyleTemplateDescriptor
from Products.PloneMeeting.profiles import UserDescriptor

import os


today = DateTime().strftime('%Y/%m/%d')

# Annex types -------------------------------------------------------------------
annexe = ItemAnnexTypeDescriptor('annexe', 'Annexe', u'attach.png')
annexeBudget = ItemAnnexTypeDescriptor('annexeBudget', 'Article Budgétaire', u'budget.png')
annexeCahier = ItemAnnexTypeDescriptor('annexeCahier', 'Cahier des Charges', u'cahier.png')
annexeDecision = ItemAnnexTypeDescriptor('annexeDecision', 'Annexe à la décision',
                                         u'attach.png', relatedTo='item_decision')
annexeDecisionToSign = ItemAnnexTypeDescriptor(
    'annexeDecisionToSign', 'Délibération à signer',
    u'deliberation_to_sign.png', relatedTo='item_decision', enabled=False)
annexeDecisionSigned = ItemAnnexTypeDescriptor(
    'annexeDecisionSigned', 'Délibération signée',
    u'deliberation_signed.png', relatedTo='item_decision', enabled=False)
annexeAvis = AnnexTypeDescriptor('annexeAvis', 'Annexe à un avis',
                                 u'attach.png', relatedTo='advice')
annexeAvisLegal = AnnexTypeDescriptor('annexeAvisLegal', 'Extrait article de loi',
                                      u'legalAdvice.png', relatedTo='advice')
annexeSeance = AnnexTypeDescriptor('annexe', 'Annexe', u'attach.png', relatedTo='meeting')

# Categories -------------------------------------------------------------------
categories = [CategoryDescriptor('recurrents', 'Récurrents'),
              CategoryDescriptor('divers', 'Divers')]

# Style Template ---------------------------------------------------------------
templates_path = os.path.join(os.path.dirname(__file__), 'templates')
stylesTemplate1 = StyleTemplateDescriptor('styles1', 'Default Styles')
stylesTemplate1.odt_file = os.path.join(templates_path, 'styles1.odt')

stylesTemplate2 = StyleTemplateDescriptor('styles2', 'Extra Styles')
stylesTemplate2.odt_file = os.path.join(templates_path, 'styles2.odt')

# Pod templates ----------------------------------------------------------------
agendaTemplate = PodTemplateDescriptor('oj', 'Ordre du jour')
agendaTemplate.odt_file = 'oj.odt'
agendaTemplate.pod_formats = ['odt', 'pdf', ]
agendaTemplate.pod_portal_types = ['Meeting']
agendaTemplate.tal_condition = u'python:tool.isManager(here)'
agendaTemplate.style_template = ['styles1']

agendaTemplateWithIndex = PodTemplateDescriptor('oj-tdm', 'Ordre du jour (Table des matières)')
agendaTemplateWithIndex.odt_file = 'oj-avec-table-des-matieres.odt'
agendaTemplateWithIndex.pod_formats = ['odt', 'pdf', ]
agendaTemplateWithIndex.pod_portal_types = ['Meeting']
agendaTemplateWithIndex.tal_condition = u'python:tool.isManager(here)'
agendaTemplateWithIndex.style_template = ['styles1']

agendaTemplateWithAnnexes = PodTemplateDescriptor('oj-annexes', 'Ordre du jour (avec annexes)')
agendaTemplateWithAnnexes.odt_file = 'oj-avec-annexes.odt'
agendaTemplateWithAnnexes.pod_formats = ['odt', 'pdf', ]
agendaTemplateWithAnnexes.pod_portal_types = ['Meeting']
agendaTemplateWithAnnexes.tal_condition = u'python:tool.isManager(here)'
agendaTemplateWithAnnexes.style_template = ['styles1']

decisionsTemplate = PodTemplateDescriptor('pv', 'Procès-verbal')
decisionsTemplate.odt_file = 'pv.odt'
decisionsTemplate.pod_formats = ['odt', 'pdf', ]
decisionsTemplate.pod_portal_types = ['Meeting']
decisionsTemplate.tal_condition = u'python:tool.isManager(here)'
decisionsTemplate.style_template = ['styles1']

attendeesTemplate = PodTemplateDescriptor('attendees', 'Exemple assemblées')
attendeesTemplate.odt_file = 'attendees.odt'
attendeesTemplate.pod_formats = ['odt', 'pdf', ]
attendeesTemplate.pod_portal_types = ['Meeting', 'MeetingItem']
attendeesTemplate.tal_condition = u'python:tool.isManager(here)'
attendeesTemplate.style_template = ['styles1']

itemTemplate = PodTemplateDescriptor('deliberation', 'Délibération')
itemTemplate.is_reusable = True
itemTemplate.odt_file = 'deliberation.odt'
itemTemplate.pod_formats = ['odt', 'pdf', ]
itemTemplate.pod_portal_types = ['MeetingItem']
itemTemplate.style_template = ['styles1']

itemTemplate_duplex = PodTemplateDescriptor('deliberation_duplex', 'Délibération (Recto/Verso)')
itemTemplate_duplex.is_reusable = True
itemTemplate_duplex.odt_file = 'deliberation_recto_verso.odt'
itemTemplate_duplex.pod_formats = ['odt', 'pdf', ]
itemTemplate_duplex.pod_portal_types = ['MeetingItem']
itemTemplate_duplex.style_template = ['styles1']

itemReport = PodTemplateDescriptor('report', 'Rapport')
itemReport.odt_file = 'report.odt'
itemReport.pod_formats = ['odt', 'pdf', ]
itemReport.pod_portal_types = ['MeetingItem']
itemReport.style_template = ['styles2']

all_delib_duplex = PodTemplateDescriptor('all_delib_duplex', 'Toutes les délibérations (Recto/Verso)')
all_delib_duplex.odt_file = 'all_delib_recto_verso.odt'
all_delib_duplex.pod_formats = ['odt', 'pdf', ]
all_delib_duplex.pod_portal_types = ['Meeting']
all_delib_duplex.tal_condition = u'python:tool.isManager(here)'
all_delib_duplex.merge_templates = [{'pod_context_name': u'delib',
                                     'do_rendering': False,
                                     'template': 'deliberation_duplex'}]

all_delib = PodTemplateDescriptor('all_delib', 'Toutes les délibérations')
all_delib.odt_file = 'all_delib.odt'
all_delib.pod_formats = ['odt', 'pdf', ]
all_delib.pod_portal_types = ['Meeting']
all_delib.tal_condition = u'python:tool.isManager(here)'
all_delib.merge_templates = [{'pod_context_name': u'delib',
                              'do_rendering': False,
                              'template': 'deliberation'}]

dfAdviceTemplate = PodTemplateDescriptor('avis-df', 'Avis DF')
dfAdviceTemplate.odt_file = 'avis-df.odt'
dfAdviceTemplate.pod_formats = ['odt', 'pdf', ]
dfAdviceTemplate.pod_portal_types = ['MeetingItem']
dfAdviceTemplate.tal_condition = u'python: context.adapted().showFinanceAdviceTemplate()'
dfAdviceTemplate.style_template = ['styles1']

dfAdvicesTemplate = PodTemplateDescriptor('synthese-avis-df-odt', 'Synthèse Avis DF', dashboard=True)
dfAdvicesTemplate.odt_file = 'synthese-avis-df.odt'
dfAdvicesTemplate.pod_formats = ['odt', 'pdf', ]
dfAdvicesTemplate.dashboard_collections_ids = [FINANCE_ADVICES_COLLECTION_ID]
dfAdvicesTemplate.style_template = ['styles1']

dashboardTemplate = PodTemplateDescriptor('recapitulatif', 'Récapitulatif', dashboard=True)
dashboardTemplate.odt_file = 'recapitulatif-tb.odt'
dashboardTemplate.tal_condition = u'python: context.absolute_url().endswith("/searches_items")'
dashboardTemplate.style_template = ['styles1']

dashboardExportTemplate = PodTemplateDescriptor('export', 'Export', dashboard=True)
dashboardExportTemplate.odt_file = 'dashboard.ods'
dashboardExportTemplate.pod_formats = ['ods', 'xls', ]
dashboardExportTemplate.tal_condition = u'python: context.absolute_url().endswith("/searches_items")'

dashboardTemplateOds = PodTemplateDescriptor('recapitulatifods', 'Récapitulatif', dashboard=True)
dashboardTemplateOds.odt_file = 'recapitulatif-tb.ods'
dashboardTemplateOds.pod_formats = ['ods', 'xls', ]
dashboardTemplateOds.tal_condition = u'python: context.absolute_url().endswith("/searches_items")'

dashboardDFTemplateOds = PodTemplateDescriptor('synthese-avis-df-ods', 'Synthèse avis DF', dashboard=True)
dashboardDFTemplateOds.odt_file = 'synthese-df-tb.ods'
dashboardDFTemplateOds.pod_formats = ['ods', 'xls', ]
dashboardDFTemplateOds.dashboard_collections_ids = [FINANCE_ADVICES_COLLECTION_ID]

dashboardMeetingAssemblies = PodTemplateDescriptor(
    'meeting-assemblies', 'Assemblée des séances', dashboard=True)
dashboardMeetingAssemblies.odt_file = 'meeting_assemblies.odt'
dashboardMeetingAssemblies.pod_formats = ['doc', 'pdf', ]
dashboardMeetingAssemblies.tal_condition = u'python:False'
dashboardMeetingAssemblies.roles_bypassing_talcondition = set(['Manager', 'MeetingManager'])
dashboardMeetingAssemblies.dashboard_collections_ids = ['searchallmeetings']

dashboardMeetingAttendances = PodTemplateDescriptor(
    'attendance-stats', 'Statistiques de présences', dashboard=True)
dashboardMeetingAttendances.odt_file = 'attendance-stats.ods'
dashboardMeetingAttendances.pod_formats = ['ods', 'xls']
dashboardMeetingAttendances.tal_condition = u'python:False'
dashboardMeetingAttendances.roles_bypassing_talcondition = set(['Manager', 'MeetingManager'])
dashboardMeetingAttendances.dashboard_collections_ids = ['searchallmeetings']

dashboardPvs = PodTemplateDescriptor('all_pv', 'Tous les Procès-Verbaux', dashboard=True)
dashboardPvs.odt_file = 'all_pv.odt'
dashboardPvs.pod_formats = ['doc', 'pdf', ]
dashboardPvs.roles_bypassing_talcondition = set(['Manager', 'MeetingManager'])
dashboardPvs.dashboard_collections_ids = ['searchallmeetings']
dashboardPvs.merge_templates = [{'pod_context_name': u'pv', 'do_rendering': False, 'template': 'pv'}]

historyTemplate = PodTemplateDescriptor('historique', 'Historique')
historyTemplate.odt_file = 'history.odt'
historyTemplate.pod_formats = ['odt', 'pdf', ]
historyTemplate.pod_portal_types = ['MeetingItem']

collegeStyleTemplate = [stylesTemplate1, stylesTemplate2]
collegeTemplates = [agendaTemplate, agendaTemplateWithIndex, agendaTemplateWithAnnexes,
                    decisionsTemplate, attendeesTemplate,
                    itemTemplate, itemTemplate_duplex, itemReport, dfAdviceTemplate,
                    dfAdvicesTemplate, dashboardTemplate,
                    dashboardTemplateOds, dashboardExportTemplate, dashboardDFTemplateOds,
                    historyTemplate, dashboardMeetingAssemblies, dashboardMeetingAttendances,
                    all_delib, all_delib_duplex, dashboardPvs]

# Users and groups -------------------------------------------------------------
dgen = UserDescriptor('dgen', [], email="test@test.be", fullname="Henry Directeur")
bourgmestre = UserDescriptor('bourgmestre', [], email="test@test.be", fullname="Pierre Bourgmestre")
dfin = UserDescriptor('dfin', [], email="test@test.be", fullname="Directeur Financier")
agentInfo = UserDescriptor('agentInfo', [], email="test@test.be", fullname="Agent Service Informatique")
agentCompta = UserDescriptor('agentCompta', [], email="test@test.be", fullname="Agent Service Comptabilité")
agentPers = UserDescriptor('agentPers', [], email="test@test.be", fullname="Agent Service du Personnel")
agentTrav = UserDescriptor('agentTrav', [], email="test@test.be", fullname="Agent Travaux")
chefPers = UserDescriptor('chefPers', [], email="test@test.be", fullname="Chef Personnel")
chefCompta = UserDescriptor('chefCompta', [], email="test@test.be", fullname="Chef Comptabilité")
echevinPers = UserDescriptor('echevinPers', [], email="test@test.be", fullname="Echevin du Personnel")
echevinTrav = UserDescriptor('echevinTrav', [], email="test@test.be", fullname="Echevin des Travaux")
conseiller = UserDescriptor('conseiller', [], email="test@test.be", fullname="Conseiller")

emetteuravisPers = UserDescriptor('emetteuravisPers', [], email="test@test.be", fullname="Emetteur avis Personnel")

groups = [OrgDescriptor('dirgen', 'Directeur général', u'DG'),
          OrgDescriptor('secretariat', 'Secrétariat général', u'Secr', groups_in_charge=['dirgen']),
          OrgDescriptor('informatique', 'Service informatique', u'Info'),
          OrgDescriptor('personnel', 'Service du personnel', u'Pers'),
          OrgDescriptor('dirfin', 'Directeur Financier', u'DF'),
          OrgDescriptor('comptabilite', 'Service comptabilité', u'Compt'),
          OrgDescriptor('travaux', 'Service travaux', u'Trav'), ]

# MeetingManager
groups[0].creators.append(dgen)
groups[0].reviewers.append(dgen)
groups[0].observers.append(dgen)
groups[0].advisers.append(dgen)

groups[1].creators.append(dgen)
groups[1].reviewers.append(dgen)
groups[1].observers.append(dgen)
groups[1].advisers.append(dgen)

groups[2].creators.append(agentInfo)
groups[2].creators.append(dgen)
groups[2].reviewers.append(agentInfo)
groups[2].reviewers.append(dgen)
groups[2].observers.append(agentInfo)
groups[2].advisers.append(agentInfo)

groups[3].creators.append(agentPers)
groups[3].observers.append(agentPers)
groups[3].creators.append(dgen)
groups[3].reviewers.append(dgen)
groups[3].creators.append(chefPers)
groups[3].reviewers.append(chefPers)
groups[3].observers.append(chefPers)
groups[3].observers.append(echevinPers)
groups[3].advisers.append(emetteuravisPers)

groups[4].creators.append(dfin)
groups[4].reviewers.append(dfin)
groups[4].observers.append(dfin)
groups[4].advisers.append(dfin)

groups[5].creators.append(agentCompta)
groups[5].creators.append(chefCompta)
groups[5].creators.append(dfin)
groups[5].creators.append(dgen)
groups[5].reviewers.append(chefCompta)
groups[5].reviewers.append(dfin)
groups[5].reviewers.append(dgen)
groups[5].observers.append(agentCompta)
groups[5].advisers.append(chefCompta)
groups[5].advisers.append(dfin)

groups[6].creators.append(agentTrav)
groups[6].creators.append(dgen)
groups[6].reviewers.append(agentTrav)
groups[6].reviewers.append(dgen)
groups[6].observers.append(agentTrav)
groups[6].observers.append(echevinTrav)
groups[6].advisers.append(agentTrav)

# Meeting configurations -------------------------------------------------------
# college
collegeMeeting = MeetingConfigDescriptor(
    'meeting-config-college', 'Collège Communal',
    'Collège communal', isDefault=True)
collegeMeeting.meetingManagers = ['dgen', ]
collegeMeeting.assembly = 'Pierre Dupont - Bourgmestre,\n' \
                          'Charles Exemple - 1er Echevin,\n' \
                          'Echevin Un, Echevin Deux, Echevin Trois - Echevins,\n' \
                          'Jacqueline Exemple, Responsable du CPAS'
collegeMeeting.signatures = 'Le Directeur général\nPierre Dupont\nLe Bourgmestre\nCharles Exemple'
collegeMeeting.certifiedSignatures = [
    {'signatureNumber': '1',
     'name': u'Mr Vraiment Présent',
     'function': u'Le Directeur général',
     'held_position': '_none_',
     'date_from': '',
     'date_to': '',
     },
    {'signatureNumber': '2',
     'name': u'Mr Charles Exemple',
     'function': u'Le Bourgmestre',
     'held_position': '_none_',
     'date_from': '',
     'date_to': '',
     },
]
collegeMeeting.places = """Place1\r
Place2\r
Place3\r"""
collegeMeeting.categories = categories
collegeMeeting.shortName = 'College'
collegeMeeting.annexTypes = [annexe, annexeBudget, annexeCahier,
                             annexeDecision, annexeDecisionToSign, annexeDecisionSigned,
                             annexeAvis, annexeAvisLegal,
                             annexeSeance]
collegeMeeting.usedItemAttributes = ['description',
                                     'motivation',
                                     'budgetInfos',
                                     'observations',
                                     'toDiscuss',
                                     'itemIsSigned',
                                     'notes',
                                     'marginalNotes',
                                     'inAndOutMoves',
                                     'otherMeetingConfigsClonableToPrivacy',
                                     'manuallyLinkedItems']
collegeMeeting.usedMeetingAttributes = ['startDate',
                                        'endDate',
                                        'attendees',
                                        'excused',
                                        'absents',
                                        'signatories',
                                        'place',
                                        'observations',
                                        'notes',
                                        'inAndOutMoves']
collegeMeeting.recordMeetingHistoryStates = []
collegeMeeting.itemColumns = ['Creator', 'CreationDate', 'ModificationDate', 'review_state',
                              'getProposingGroup', 'advices', 'linkedMeetingDate',
                              'getItemIsSigned', 'actions']
collegeMeeting.availableItemsListVisibleColumns = [
    'Creator', 'CreationDate', 'getProposingGroup', 'advices', 'actions']
collegeMeeting.itemsListVisibleColumns = [
    u'static_item_reference', u'Creator', u'CreationDate', u'review_state',
    u'getProposingGroup', u'advices', u'actions']
collegeMeeting.xhtmlTransformFields = ()
collegeMeeting.xhtmlTransformTypes = ()
collegeMeeting.itemWorkflow = 'meetingitemcommunes_workflow'
collegeMeeting.meetingWorkflow = 'meetingcommunes_workflow'
collegeMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowConditions'
collegeMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowActions'
collegeMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowConditions'
collegeMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowActions'
collegeMeeting.transitionsToConfirm = ('MeetingItem.accept_but_modify', 'MeetingItem.propose',
                                       'MeetingItem.refuse', 'MeetingItem.backToItemCreated',
                                       'MeetingItem.backToProposed',
                                       'MeetingItem.backTo_itemfrozen_from_returned_to_proposing_group',
                                       'MeetingItem.backTo_presented_from_returned_to_proposing_group',
                                       'MeetingItem.delay', 'MeetingItem.backToValidated',
                                       'MeetingItem.validate', 'MeetingItem.return_to_proposing_group')
collegeMeeting.meetingTopicStates = ('created', 'frozen')
collegeMeeting.decisionTopicStates = ('decided', 'closed')
collegeMeeting.enforceAdviceMandatoriness = False
collegeMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                             'reverse': '0'}, )
collegeMeeting.recordItemHistoryStates = []
collegeMeeting.maxShownMeetings = 5
collegeMeeting.maxDaysDecisions = 60
collegeMeeting.meetingAppDefaultView = 'searchmyitems'
collegeMeeting.enableLabels = False
collegeMeeting.defaultLabels = [
    {'color': 'purple-light', 'by_user': False, 'title': 'À délai'},
    {'color': 'orange', 'by_user': False, 'title': 'Attention'},
    {'color': 'cadetblue', 'by_user': False, 'title': 'En attente'},
    {'color': 'cornflowerblue', 'by_user': False, 'title': 'Bloqué'},
    {'color': 'green-light', 'by_user': False, 'title': 'OK'},
    {'color': 'green', 'by_user': True, 'title': 'Lu'},
    {'color': 'yellow', 'by_user': True, 'title': 'Suivi'},
    {'color': 'red', 'by_user': False, 'title': 'Urgent'}]
collegeMeeting.useAdvices = True
collegeMeeting.selectableAdvisers = ['comptabilite', 'dirfin', 'dirgen', 'informatique',
                                     'personnel', 'secretariat', 'travaux']
collegeMeeting.itemAdviceStates = ('validated',)
collegeMeeting.itemAdviceEditStates = ('validated',)
collegeMeeting.itemAdviceViewStates = ('validated',
                                       'presented',
                                       'itemfrozen',
                                       'accepted',
                                       'refused',
                                       'accepted_but_modified',
                                       'delayed',
                                       'pre_accepted',)
collegeMeeting.usedAdviceTypes = ['positive', 'positive_with_remarks', 'negative', 'nil', ]
collegeMeeting.enableAdviceInvalidation = False
collegeMeeting.itemAdviceInvalidateStates = []
collegeMeeting.customAdvisers = [
    {'row_id': 'unique_id_001',
     'org': 'comptabilite',
     'gives_auto_advice_on': 'item/getBudgetRelated',
     'for_item_created_from': today,
     'is_linked_to_previous_row': '0'},
    {'row_id': 'unique_id_002',
     'org': 'dirfin',
     'for_item_created_from': today,
     'delay': '5',
     'delay_left_alert': '2',
     'delay_label': 'Incidence financière >= 22.000€',
     'is_linked_to_previous_row': '0'},
    {'row_id': 'unique_id_003',
     'org': 'dirfin',
     'for_item_created_from': today,
     'delay': '10',
     'delay_left_alert': '4',
     'delay_label': 'Incidence financière >= 22.000€',
     'is_linked_to_previous_row': '1'},
    {'row_id': 'unique_id_004',
     'org': 'dirfin',
     'for_item_created_from': today,
     'delay': '20',
     'delay_left_alert': '4',
     'delay_label': 'Incidence financière >= 22.000€',
     'is_linked_to_previous_row': '1'},
    {'row_id': 'unique_id_005',
     'org': 'dirgen',
     'gives_auto_advice_on': 'python: item.getGroupsInCharge(fromOrgIfEmpty=True, first=True) == org_uid',
     'gives_auto_advice_on_help_message': "Le groupe \xc3\xa9metteur d'avis est en charge du groupe proposant du point",
     'for_item_created_from': today,
     'delay': '',
     'delay_left_alert': '',
     'delay_label': '',
     'is_linked_to_previous_row': '0'},
]
collegeMeeting.powerObservers = (
    {'row_id': 'powerobservers',
     'label': 'Super observateurs',
     'item_states': ('itemfrozen',
                     'accepted',
                     'delayed',
                     'refused',
                     'accepted_but_modified',
                     'pre_accepted'),
     'meeting_states': ('frozen', 'decided', 'closed'),
     'orderindex_': '1'},
    {'row_id': 'restrictedpowerobservers',
     'label': 'Super observateurs restreints',
     'item_states': ('itemfrozen',
                     'accepted',
                     'delayed',
                     'refused',
                     'accepted_but_modified',
                     'pre_accepted'),
     'meeting_states': ('frozen', 'decided', 'closed'),
     'orderindex_': '2'})

collegeMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
collegeMeeting.workflowAdaptations = [
    'no_publication', 'no_global_observation',
    'return_to_proposing_group', 'refused',
    'presented_item_back_to_itemcreated', 'presented_item_back_to_proposed',
    'only_creator_may_delete']
collegeMeeting.transitionsForPresentingAnItem = ('propose', 'validate', 'present', )
collegeMeeting.onTransitionFieldTransforms = (
    ({'transition': 'delay',
      'field_name': 'MeetingItem.decision',
      'tal_expression': "string:<p>Le Collège décide de reporter le point.</p>${here/getDecision}"},))
collegeMeeting.onMeetingTransitionItemActionToExecute = (
    {'meeting_transition': 'freeze',
     'item_action': 'itemfreeze',
     'tal_expression': ''},

    {'meeting_transition': 'decide',
     'item_action': 'itemfreeze',
     'tal_expression': ''},

    {'meeting_transition': 'publish_decisions',
     'item_action': 'itemfreeze',
     'tal_expression': ''},
    {'meeting_transition': 'publish_decisions',
     'item_action': 'accept',
     'tal_expression': ''},

    {'meeting_transition': 'close',
     'item_action': 'itemfreeze',
     'tal_expression': ''},
    {'meeting_transition': 'close',
     'item_action': 'accept',
     'tal_expression': ''},)
collegeMeeting.powerAdvisersGroups = ('dirgen', 'dirfin', )
collegeMeeting.itemBudgetInfosStates = ('proposed', 'validated', 'presented')
collegeMeeting.useCopies = True
collegeMeeting.selectableCopyGroups = [groups[0].getIdSuffixed('reviewers'),
                                       groups[1].getIdSuffixed('reviewers'),
                                       groups[2].getIdSuffixed('reviewers'),
                                       groups[4].getIdSuffixed('reviewers')]
collegeMeeting.styleTemplates = collegeStyleTemplate
collegeMeeting.podTemplates = collegeTemplates
collegeMeeting.meetingConfigsToCloneTo = [{'meeting_config': 'cfg2',
                                           'trigger_workflow_transitions_until': '__nothing__'}, ]
collegeMeeting.itemAutoSentToOtherMCStates = ('accepted', 'accepted_but_modified', )
collegeMeeting.recurringItems = [
    RecurringItemDescriptor(
        id='recurringagenda1',
        title='Approuve le procès-verbal de la séance antérieure',
        description='<p>Approuve le procès-verbal de la séance antérieure</p>',
        category='recurrents',
        proposingGroup='secretariat',
        decision='<p>Procès-verbal approuvé</p>'),
    RecurringItemDescriptor(
        id='recurringofficialreport1',
        title='Autorise et signe les bons de commande de la semaine',
        description='<p>Autorise et signe les bons de commande de la semaine</p>',
        category='recurrents',
        proposingGroup='secretariat',
        decision='<p>Bons de commande signés</p>'),
    RecurringItemDescriptor(
        id='recurringofficialreport2',
        title='Ordonnance et signe les mandats de paiement de la semaine',
        description='<p>Ordonnance et signe les mandats de paiement de la semaine</p>',
        category='recurrents',
        proposingGroup='secretariat',
        decision='<p>Mandats de paiement de la semaine approuvés</p>'), ]
collegeMeeting.itemTemplates = [
    ItemTemplateDescriptor(
        id='template1',
        title='Tutelle CPAS',
        description='<p>Tutelle CPAS</p>',
        category='personnel',
        proposingGroup='secretariat',
        templateUsingGroups=['secretariat', 'dirgen', ],
        decision="""<p>Vu la loi du 8 juillet 1976 organique des centres publics d'action sociale
 et plus particulièrement son article 111;</p>
<p>Vu l'Arrêté du Gouvernement Wallon du 22 avril 2004 portant codification de la législation
 relative aux pouvoirs locaux tel que confirmé par le décret du 27 mai 2004 du Conseil régional wallon;</p>
<p>Attendu que les décisions suivantes du Bureau permanent/du Conseil de l'Action sociale du
 XXX ont été reçues le XXX dans le cadre de la tutelle générale sur les centres publics d'action sociale :</p>
<p>- ...;</p>
<p>- ...;</p>
<p>- ...</p>
<p>Attendu que ces décisions sont conformes à la loi et à l'intérêt général;</p>
<p>Déclare à l'unanimité que :</p>
<p><strong>Article 1er :</strong></p>
<p>Les décisions du Bureau permanent/Conseil de l'Action sociale visées ci-dessus sont conformes
 à la loi et à l'intérêt général et qu'il n'y a, dès lors, pas lieu de les annuler.</p>
<p><strong>Article 2 :</strong></p>
<p>Copie de la présente délibération sera transmise au Bureau permanent/Conseil de l'Action sociale.</p>"""),
    ItemTemplateDescriptor(
        id='template2',
        title='Contrôle médical systématique agent contractuel',
        description='<p>Contrôle médical systématique agent contractuel</p>',
        category='personnel',
        proposingGroup='personnel',
        templateUsingGroups=['personnel', ],
        decision="""
            <p>Vu la loi du 26 mai 2002 instituant le droit à l’intégration sociale;</p>
<p>Vu la délibération du Conseil communal du 29 juin 2009 concernant le cahier spécial des
 charges relatif au marché de services portant sur le contrôle des agents communaux absents pour raisons médicales;</p>
<p>Vu sa délibération du 17 décembre 2009 désignant le docteur XXX en qualité d’adjudicataire
 pour la mission de contrôle médical des agents de l’Administration communale;</p>
<p>Vu également sa décision du 17 décembre 2009 d’opérer les contrôles médicaux de manière
 systématique et pour une période d’essai d’un trimestre;</p>
<p>Attendu qu’un certificat médical a été  reçu le XXX concernant XXX la couvrant du XXX au XXX,
 avec la mention « XXX »;</p>
<p>Attendu que le Docteur XXX a transmis au service du Personnel, par fax, le même jour à XXX le rapport de
 contrôle mentionnant l’absence de XXX ce XXX à XXX;</p>
<p>Considérant que XXX avait été informée par le Service du Personnel de la mise en route du système
 de contrôle systématique que le médecin-contrôleur;</p>
<p>Considérant qu’ayant été absent(e) pour maladie la semaine précédente elle avait reçu la visite du
 médecin-contrôleur;</p>
<p>DECIDE :</p>
<p><strong>Article 1</strong> : De convoquer XXX devant  Monsieur le Secrétaire communal f.f. afin de lui
 rappeler ses obligations en la matière.</p>
<p><strong>Article 2</strong> :  De prévenir XXX, qu’en cas de récidive, il sera proposé par le Secrétaire
 communal au Collège de transformer les jours de congés de maladie en absence injustifiée (retenue sur traitement
 avec application de la loi du 26 mai 2002 citée ci-dessus).</p>
<p><strong>Article 3</strong> : De charger le service du personnel du suivi de ce dossier.</p>"""),
    ItemTemplateDescriptor(
        id='template3',
        title='Engagement temporaire',
        description='<p>Engagement temporaire</p>',
        category='personnel',
        proposingGroup='personnel',
        templateUsingGroups=['personnel', ],
        decision="""<p>Considérant qu’il y a lieu de pourvoir au remplacement de Madame XXX,
 XXX bénéficiant d’une interruption de carrière pour convenances personnelles pour l’année scolaire
 2009/2010. &nbsp;</p>
<p>Attendu qu’un appel public a été lancé au mois de mai dernier;</p>
<p>Vu la circulaire N° 2772 de la Communauté Française&nbsp;du 29 juin 2009 concernant &nbsp;la gestion des
 carrières administrative et pécuniaire dans l’enseignement fondamental ordinaire et principalement le chapitre 3
 relatif aux engagements temporaires pendant l’année scolaire 2009/2010;</p>
<p>Vu la proposition du directeur concerné d’attribuer cet emploi à Monsieur XXX, titulaire des titres requis;</p>
<p>Vu le décret de la Communauté Française du 13 juillet 1998 portant restructuration de l’enseignement&nbsp;maternel
 et primaire ordinaires avec effet au 1er octobre 1998;</p>
<p>Vu la loi du 29 mai 1959 (Pacte scolaire) et les articles L1122-19 et L1213-1 du Code de la démocratie locale et
 de la décentralisation;</p>
<p>Vu l’avis favorable de l’Echevin de l’Enseignement;</p>
<p><b>DECIDE&nbsp;:</b><br>
<b><br> Article 1<sup>er</sup></b> :</p>
<p>Au scrutin secret et à l’unanimité, de désigner Monsieur XXX, né le XXX à XXX et domicilié à XXX, en qualité
 d’instituteur maternel temporaire mi-temps en remplacement de Madame XXX aux écoles communales fondamentales de
 Sambreville (section de XXX) du XXX au XXX.</p>
<p><b>Article 2</b> :</p>
<p>L’horaire hebdomadaire de l’intéressé est fixé à 13 périodes.</p>
<p><b>Article 3&nbsp;:</b></p>
<p>La présente délibération sera soumise à la ratification du Conseil Communal. Elle sera transmise au
 Bureau Régional de l’Enseignement primaire et maternel, à l’Inspectrice Cantonale et à la direction concernée.</p>"""),
    ItemTemplateDescriptor(
        id='template4',
        title='Prestation réduite',
        description='<p>Prestation réduite</p>',
        category='personnel',
        proposingGroup='personnel',
        templateUsingGroups=['personnel', ],
        decision="""<p>Vu la loi de redressement du 22 janvier 1985 (article 99 et suivants) et de l’Arrêté Royal du
         12 août 1991 (tel que modifié) relatifs à l’interruption de carrière professionnelle dans l’enseignement;</p>
<p>Vu la lettre du XXX par laquelle Madame XXX, institutrice maternelle, sollicite le renouvellement pendant l’année
 scolaire 2009/2010 de son congé pour prestations réduites mi-temps pour convenances personnelles dont elle bénéficie
 depuis le 01 septembre 2006;</p>
<p>Attendu que le remplacement de l’intéressée&nbsp;est assuré pour la prochaine rentrée scolaire;</p>
<p>Vu le décret de la Communauté Française du 13 juillet 1988 portant restructuration de l’enseignement maternel et
 primaire ordinaires avec effet au 1er octobre 1998;</p>
<p>Vu la loi du 29 mai 1959 (Pacte Scolaire) et les articles L1122-19 et L1213-1 du code de la démocratie locale et
 de la décentralisation;</p>
<p>Vu l’avis favorable de l’Echevin de l’Enseignement;</p>
<p><b>DECIDE&nbsp;:</b><br><b><br> Article 1<sup>er</sup></b>&nbsp;:</p>
<p>Au scrutin secret et à l’unanimité, d’accorder à Madame XXX le congé pour prestations réduites mi-temps sollicité
 pour convenances personnelles en qualité d’institutrice maternelle aux écoles communales
 fondamentales&nbsp;&nbsp;de Sambreville (section de XXX).</p>
<p><b>Article 2</b> :</p>
<p>Une activité lucrative est autorisée durant ce congé qui est assimilé à une période d’activité de service, dans
 le respect de la réglementation relative au cumul.</p>
<p><b>Article 3&nbsp;:</b></p>
<p>La présente délibération sera soumise pour accord au prochain Conseil, transmise au Bureau Régional de
 l’Enseignement primaire et maternel, à&nbsp;l’Inspectrice Cantonale, à la direction
 concernée et à l’intéressée.</p>"""),
    ItemTemplateDescriptor(
        id='template5',
        title='Exemple modèle disponible pour tous',
        description='<p>Exemple modèle disponible pour tous</p>',
        category='personnel',
        proposingGroup='',
        templateUsingGroups=[],
        decision="""<p>Vu la loi du XXX;</p>
<p>Vu ...;</p>
<p>Attendu que ...;</p>
<p>Vu le décret de la Communauté Française du ...;</p>
<p>Vu la loi du ...;</p>
<p>Vu l’avis favorable de ...;</p>
<p><b>DECIDE&nbsp;:</b><br><b><br> Article 1<sup>er</sup></b>&nbsp;:</p>
<p>...</p>
<p><b>Article 2</b> :</p>
<p>...</p>
<p><b>Article 3&nbsp;:</b></p>
<p>...</p>"""),
]
collegeMeeting.addContactsCSV = True

# Conseil communal
# Pod templates ----------------------------------------------------------------
agendaCouncilTemplate = PodTemplateDescriptor('oj', 'Ordre du jour')
agendaCouncilTemplate.odt_file = 'council-oj.odt'
agendaCouncilTemplate.pod_formats = ['odt', 'pdf', ]
agendaCouncilTemplate.pod_portal_types = ['Meeting']
agendaCouncilTemplate.tal_condition = u'python:tool.isManager(here)'
agendaCouncilTemplate.style_template = ['styles1']

decisionsCouncilTemplate = PodTemplateDescriptor('pv', 'Procès-verbal')
decisionsCouncilTemplate.odt_file = 'council-pv.odt'
decisionsCouncilTemplate.pod_formats = ['odt', 'pdf', ]
decisionsCouncilTemplate.pod_portal_types = ['Meeting']
decisionsCouncilTemplate.tal_condition = u'python:tool.isManager(here)'
decisionsCouncilTemplate.style_template = ['styles1']

itemCouncilRapportTemplate = PodTemplateDescriptor('rapport', 'Rapport')
itemCouncilRapportTemplate.odt_file = 'council-rapport.odt'
itemCouncilRapportTemplate.pod_formats = ['odt', 'pdf', ]
itemCouncilRapportTemplate.pod_portal_types = ['MeetingItem']
itemCouncilRapportTemplate.tal_condition = u''
itemCouncilRapportTemplate.style_template = ['styles1']

itemCouncilTemplate = PodTemplateDescriptor('deliberation', 'Délibération')
itemCouncilTemplate.pod_template_to_use = {'cfg_id': collegeMeeting.id, 'template_id': itemTemplate.id}
itemCouncilTemplate.pod_formats = ['odt', 'pdf', ]
itemCouncilTemplate.pod_portal_types = ['MeetingItem']
itemCouncilTemplate.style_template = ['styles1']

councilStyleTemplate = [stylesTemplate1]

councilTemplates = [agendaCouncilTemplate, decisionsCouncilTemplate,
                    itemCouncilRapportTemplate, itemCouncilTemplate,
                    dashboardTemplate, dashboardMeetingAssemblies, dashboardMeetingAttendances]

councilMeeting = MeetingConfigDescriptor(
    'meeting-config-council', 'Conseil Communal',
    'Conseil Communal')
councilMeeting.meetingManagers = ['dgen', ]
councilMeeting.certifiedSignatures = [
    {'signatureNumber': '1',
     'name': u'Mr Vraiment Présent',
     'function': u'Le Secrétaire communal',
     'held_position': '_none_',
     'date_from': '',
     'date_to': '',
     },
    {'signatureNumber': '2',
     'name': u'Mr Charles Exemple',
     'function': u'Le Bourgmestre',
     'held_position': '_none_',
     'date_from': '',
     'date_to': '',
     },
]
councilMeeting.places = """Place1\n\r
Place2\n\r
Place3\n\r"""
councilMeeting.categories = categories
councilMeeting.shortName = 'Council'
councilMeeting.annexTypes = [annexe, annexeBudget, annexeCahier,
                             annexeDecision, annexeDecisionToSign, annexeDecisionSigned,
                             annexeAvis, annexeAvisLegal,
                             annexeSeance]
councilMeeting.usedItemAttributes = ['description',
                                     'motivation',
                                     'oralQuestion',
                                     'itemInitiator',
                                     'observations',
                                     'privacy',
                                     'notes',
                                     'marginalNotes',
                                     'inAndOutMoves',
                                     'manuallyLinkedItems']
councilMeeting.usedMeetingAttributes = ['startDate',
                                        'midDate',
                                        'endDate',
                                        'attendees',
                                        'excused',
                                        'absents',
                                        'signatories',
                                        'replacements',
                                        'place',
                                        'observations',
                                        'notes',
                                        'inAndOutMoves']
councilMeeting.recordMeetingHistoryStates = []
councilMeeting.xhtmlTransformFields = ('MeetingItem.description',
                                       'MeetingItem.motivation',
                                       'MeetingItem.decision',
                                       'MeetingItem.observations',
                                       'Meeting.observations', )
councilMeeting.xhtmlTransformTypes = ('removeBlanks',)
councilMeeting.itemWorkflow = 'meetingitemcommunes_workflow'
councilMeeting.meetingWorkflow = 'meetingcommunes_workflow'
councilMeeting.itemConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowConditions'
councilMeeting.itemActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingItemCommunesWorkflowActions'
councilMeeting.meetingConditionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowConditions'
councilMeeting.meetingActionsInterface = 'Products.MeetingCommunes.interfaces.IMeetingCommunesWorkflowActions'
councilMeeting.transitionsToConfirm = ('MeetingItem.accept_but_modify', 'MeetingItem.propose',
                                       'MeetingItem.refuse', 'MeetingItem.backToItemCreated',
                                       'MeetingItem.backToProposed',
                                       'MeetingItem.backTo_itemfrozen_from_returned_to_proposing_group',
                                       'MeetingItem.backTo_presented_from_returned_to_proposing_group',
                                       'MeetingItem.delay', 'MeetingItem.backToValidated',
                                       'MeetingItem.validate', 'MeetingItem.return_to_proposing_group')
councilMeeting.meetingTopicStates = ('created', 'frozen')
councilMeeting.decisionTopicStates = ('decided', 'closed')
councilMeeting.itemAdviceStates = ('validated',)
councilMeeting.enforceAdviceMandatoriness = False
councilMeeting.insertingMethodsOnAddItem = ({'insertingMethod': 'on_proposing_groups',
                                             'reverse': '0'}, )
councilMeeting.recordItemHistoryStates = []
councilMeeting.maxShownMeetings = 5
councilMeeting.maxDaysDecisions = 60
councilMeeting.meetingAppDefaultView = 'searchmyitems'
councilMeeting.itemDocFormats = ('odt', 'pdf')
councilMeeting.meetingDocFormats = ('odt', 'pdf')
councilMeeting.useAdvices = False
councilMeeting.itemAdviceStates = ()
councilMeeting.itemAdviceEditStates = ()
councilMeeting.itemAdviceViewStates = ()
councilMeeting.itemDecidedStates = ['accepted', 'refused', 'delayed', 'accepted_but_modified', 'pre_accepted']
councilMeeting.workflowAdaptations = [
    'no_publication', 'no_global_observation',
    'return_to_proposing_group', 'refused',
    'presented_item_back_to_itemcreated', 'presented_item_back_to_proposed',
    'only_creator_may_delete']
councilMeeting.transitionsForPresentingAnItem = ('propose', 'validate', 'present', )
councilMeeting.onMeetingTransitionItemActionToExecute = deepcopy(
    collegeMeeting.onMeetingTransitionItemActionToExecute)
councilMeeting.powerObservers = deepcopy(collegeMeeting.powerObservers)
councilMeeting.powerAdvisersGroups = ()
councilMeeting.itemBudgetInfosStates = ('proposed', 'validated', 'presented')
councilMeeting.useCopies = True
councilMeeting.selectableCopyGroups = [groups[0].getIdSuffixed('reviewers'),
                                       groups[1].getIdSuffixed('reviewers'),
                                       groups[2].getIdSuffixed('reviewers'),
                                       groups[4].getIdSuffixed('reviewers')]
councilMeeting.styleTemplates = councilStyleTemplate
councilMeeting.podTemplates = councilTemplates

councilMeeting.recurringItems = [
    RecurringItemDescriptor(
        id='recurringagenda1',
        title='Approuve le procès-verbal de la séance antérieure',
        description='<p>Approuve le procès-verbal de la séance antérieure</p>',
        category='recurrents',
        proposingGroup='secretariat',
        decision='<p>Procès-verbal approuvé</p>'), ]
councilMeeting.itemTemplates = collegeMeeting.itemTemplates
councilMeeting.orderedContacts = ['ga-c-rard-bourgmestre/bourgmestre-mon-organisation',
                                  'isabelle-daga/dg-mon-organisation',
                                  'claudine-lapremiare/alderman-mon-organisation',
                                  'bernardette-laseconde/alderman-mon-organisation',
                                  'christian-letroisiame/alderman-mon-organisation',
                                  'henri-quattre/alderman-mon-organisation',
                                  'laurence-suivant/alderman-mon-organisation']

data = PloneMeetingConfiguration(meetingFolderTitle='Mes séances',
                                 meetingConfigs=(collegeMeeting, councilMeeting),
                                 orgs=groups)
data.usersOutsideGroups = [bourgmestre, conseiller]
data.directory_position_types = [
    {'token': u'default',
     'name': u'(Utiliser le champ "Intitulé")'},
    {'token': u'administrateur',
     'name': u'Administrateur|Administrateurs|Administratrice|Administratrices'},
    {'token': u'alderman',
     'name': u'Échevin|Échevins|Échevine|Échevines'},
    {'name': u'1er Échevin|1er Échevins|1ère Échevine|1ère Échevines',
     'token': u'alderman-1'},
    {'name': u'2ème Échevin|2èmes Échevins|2ème Échevine|2èmes Échevines',
     'token': u'alderman-2'},
    {'name': u'3ème Échevin|3èmes Échevins|3ème Échevine|3èmes Échevines',
     'token': u'alderman-3'},
    {'name': u'4ème Échevin|4èmes Échevins|4ème Échevine|4èmes Échevines',
     'token': u'alderman-4'},
    {'name': u'5ème Échevin|5èmes Échevins|5ème Échevine|5èmes Échevines',
     'token': u'alderman-5'},
    {'name': u'6ème Échevin|6èmes Échevins|6ème Échevine|6èmes Échevines',
     'token': u'alderman-6'},
    {'token': u'bourgmestre',
     'name': u'Bourgmestre|Bourgmestres|Bourgmestre|Bourgmestres'},
    {'token': u'bourgmestreff',
     'name': u'Bourgmestre f.f.|Bourgmestres f.f.|Bourgmestre f.f.|Bourgmestres f.f.'},
    {'token': u'president',
     'name': u'Président|Présidents|Présidente|Présidentes'},
    {'token': u'bourgmestre-president',
     'name': u'Bourgmestre - Président|Bourgmestres - Présidents|'
        u'Bourgmestre - Présidente|Bourgmestres - Présidentes'},
    {'token': u'bourgmestreff-president',
     'name': u'Bourgmestre f.f. - Président|Bourgmestres f.f. - Présidents|'
        u'Bourgmestre f.f. - Présidente|Bourgmestres f.f. - Présidentes'},
    {'token': u'conseiller',
     'name': u'Conseiller|Conseillers|Conseillère|Conseillères'},
    {'token': u'conseiller-president',
     'name': u'Conseiller - Président|Conseillers - Présidents|'
        u'Conseillère - Présidente|Conseillères - Présidentes'},
    {'token': u'president-cpas',
     'name': u'Président du CPAS|Présidents du CPAS|Présidente du CPAS|Présidentes du CPAS'},
    {'token': u'dg',
     'name': u'Directeur général|Directeurs généraux|'
        u'Directrice générale|Directrices générales'},
    {'token': u'dgff',
     'name': u'Directeur général f.f.|Directeurs généraux f.f.|'
        u'Directrice générale f.f.|Directrices générales f.f.'},
    {'token': u'df',
     'name': u'Directeur financier|Directeurs financiers|Directrice financière|Directrices financières'},
    {'token': u'dfff',
     'name': u'Directeur financier f.f.|Directeurs financiers f.f.|'
        u'Directrice financière f.f.|Directrices financières f.f.'},
    {'token': u'depute',
     'name': u'Député|Députés|Députée|Députées'},
    {'token': u'secretaire',
     'name': u'Secrétaire de séance|Secrétaires de séance|Secrétaire de séance|Secrétaires de séance'},
]
contactsTemplate = PodTemplateDescriptor('contactsTemplate', 'Export', dashboard=True)
contactsTemplate.odt_file = 'organizations-export.ods'
contactsTemplate.use_objects = True
contactsTemplate.pod_formats = ['ods', 'xls', ]
contactsTemplate.dashboard_collections_ids = ['all_orgs']
data.contactsTemplates = [contactsTemplate]
