from decimal import Decimal

from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from flower_app.controllers.permissions import HasGroupPermission
from .publishing import computeDocx, computePdf
from django.core.signing import Signer
from django.http import HttpResponse
from http import HTTPStatus
from flower_app.models.Etude import Etude
from flower_app.models.Facture import Facture
from flower_app.models.Mission import Mission
from flower_app.models.People.Membre import Membre
from flower_app.models.People.Realisateur import Realisateur
from flower_app.models.PVR import PVR
from flower_app.models.NdF import NdF
from flower_app.models.BV import BV
from flower_app.models.BA import BA
from datetime import date
from flower_app.controllers.gantt.gantt import computeGanttFromEtudeRaw

import tempfile

from ...models.CC import CC


class DevisView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        # from modules/etudes/components/Generation.vue in modules/etudes/views/EtudeDetails.vue
        'GET': ['ROLE_CA']
    }

    def retrieve(request, self, etude_id):
        etude = Etude.objects.get(pk=etude_id)
        return computeDocx({'etude': etude}, 'DEVIS.docx', 'DEVIS-' + etude.name)


class CustomDevisView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'POST': ['ROLE_CA']  # from modules/prospects/views/Devis.vue
    }

    def create(self, request):
        etude = request.data
        etude['projectManager'] = Membre.objects.get(
            pk=etude['projectManager'])
        return computeDocx({'etude': etude}, 'DEVIS_JSON.docx', 'DEVIS-' + etude['name'])


class CEViewDocx(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        # from modules/etudes/components/Generation.vue in modules/etudes/views/EtudeDetails.vue
        'GET': ['ROLE_CA']
    }

    def retrieve(request, self, etude_id):
        etude = Etude.objects.get(pk=etude_id)
        svgData = computeGanttFromEtudeRaw(etude)[1]
        tmp_img_file = tempfile.NamedTemporaryFile(delete=None, suffix='.jpg')
        svgData.write_image(tmp_img_file)
        images = {'gantt': tmp_img_file.name}

        total_nbJEH = 0
        total_HT = 0
        duree = 0

        phases = []
        for phase in etude.phaseEtude.all():
            total = phase.nbJEH * phase.priceJEH
            phases.append({
                "title": phase.title,
                "nbJEH": phase.nbJEH,
                "priceJEH": phase.priceJEH,
                "totalHT": total
            })
            duree += phase.period
            total_nbJEH += phase.nbJEH
            total_HT += total

        application_fees = etude.docEtude.application_fees
        if (etude.docEtude.hasMaterialFees):
            material_fees = etude.docEtude.materialFees
        total_with_fees = total_HT + application_fees
        tva = total_with_fees * Decimal(str(0.2))
        total_ttc = total_with_fees + tva
        semaines = duree/7

        context = {
            "etude": etude,
            "phases": phases,
            "total_nbJEH": total_nbJEH,
            "total_HT": total_HT,
            "total_with_fees": total_with_fees,
            "tva": tva,
            "total_ttc": total_ttc,
            "semaines": semaines,
        }

        if etude.cc is None or etude.cc == '':
            return computeDocx(context, 'CE.docx', 'CE-' + etude.name, images=images)
        else:
            return computeDocx(context, 'BC.docx', 'BC-' + etude.name, images=images)

class CEViewPdf(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        # from modules/etudes/components/Generation.vue in modules/etudes/views/EtudeDetails.vue
        'GET': ['ROLE_CA']
    }

    def retrieve(request, self, etude_id):
        etude = Etude.objects.get(pk=etude_id)
        svgData = computeGanttFromEtudeRaw(etude)[1]
        tmp_img_file = tempfile.NamedTemporaryFile(delete=None, suffix='.jpg')
        svgData.write_image(tmp_img_file)
        images = {'gantt': tmp_img_file.name}

        total_nbJEH = 0
        total_HT = 0
        duree = 0

        phases = []
        nbPhases = etude.phaseEtude.all().count()
        for phase in etude.phaseEtude.all():
            total = phase.nbJEH * phase.priceJEH
            phases.append({
                "title": phase.title,
                "nbJEH": phase.nbJEH,
                "priceJEH": phase.priceJEH,
                "totalHT": total
            })
            duree += phase.period
            total_nbJEH += phase.nbJEH
            total_HT += total

        application_fees = etude.docEtude.application_fees
        material_fees = 0
        if (etude.docEtude.hasMaterialFees):
            material_fees = etude.docEtude.materialFees
        total_with_fees = total_HT + application_fees + material_fees
        tva = total_with_fees * Decimal(str(0.2))
        total_ttc = total_with_fees + tva
        semaines = duree/7

        context = {
            "etude": etude,
            "nbPhases": nbPhases,
            "phases": phases,
            "total_nbJEH": total_nbJEH,
            "total_HT": total_HT,
            "material_fees": material_fees,
            "total_with_fees": total_with_fees,
            "tva": tva,
            "total_ttc": total_ttc,
            "semaines": semaines,
        }

        if etude.cc is None or etude.cc == '':
            print("Génération d'une CE")
            return computePdf(context, 'CE.docx', 'CE-' + etude.name, images=images)
        else:
            return computePdf(context, 'BC.docx', 'BC-' + etude.name, images=images)

class CCViewDocx(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        # from modules/etudes/components/Generation.vue in modules/etudes/views/EtudeDetails.vue
        'GET': ['ROLE_CA']
    }

    def retrieve(request, self, cc_id):
        cc = CC.objects.get(pk=cc_id)

        context = {
            "cc": cc,
        }

        return computeDocx(context, 'CCA.docx', 'CC-' + cc.name)

class CCViewPdf(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        # from modules/etudes/components/Generation.vue in modules/etudes/views/EtudeDetails.vue
        'GET': ['ROLE_CA']
    }

    def retrieve(request, self, cc_id):
        cc = CC.objects.get(pk=cc_id)
        print("CC ", cc.number)

        context = {
            "cc": cc,
        }

        return computePdf(context, 'CCA.docx', 'CC-' + cc.name)


class RDMView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        # from modules/etudes/components/Generation.vue in modules/etudes/views/EtudeDetails.vue
        'GET': ['ROLE_CA']
    }

    def retrieve(request, self, rdm_id):
        mission = Mission.objects.get(pk=rdm_id)
        rea = mission.consultant

        total_nbJEH = 0
        total_retrib = 0
        duree = 0

        nbPhases = mission.phasesMission.all().count()
        for phase in mission.phasesMission.all():
            total = phase.nbJEH * phase.priceJEH
            duree += phase.period
            total_nbJEH += phase.nbJEH
            total_retrib += total

        semaines = duree / 7

        if rea.ba != None:
            if rea.isMember:
                ref = 'RM_'+str(rea.ba.year % 100)+'C' + '%03d' % rea.ba_id+'_'+str(mission.project.number)
            else:
                ref = 'RM_' + str(rea.ba.year % 100) + 'R' + '%03d' % rea.ba_id + '_' + str(mission.project.number)
            context = {
                "rdm": {'mission': mission, 'ref': ref},
                "nbPhases": nbPhases,
                "total_nbJEH": total_nbJEH,
                "total_retrib": total_retrib,
                "semaines": semaines,
            }
            return computeDocx(context, 'RDM.docx', 'RDM-' + mission.project.name)
        else:
            return HttpResponse("Réalisateur sans BA généré", status=HTTPStatus.FORBIDDEN)



class NdFView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_TRESO']
    }

    def retrieve(request, self, ndf_id):
        ndf = NdF.objects.get(pk=ndf_id)
        return computeDocx({'ndf': ndf}, 'NF.docx', ndf.reference)


class BVView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA', 'ROLE_TRESO']
    }

    def retrieve(request, self, bv_id):
        bv = BV.objects.get(pk=bv_id)
        return computeDocx({
            'bv': bv,
            'rea': bv.rdm.consultant
        }, 'BV.docx', bv.reference)


class BAView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA']
    }

    def retrieve(request, self, etudiant_id):
        rea = Membre.objects.get(pk=etudiant_id)
        if rea.ba == None:
            rea.ba = date.today()
            if BA.objects.filter(year=rea.ba.year, type="CA").first():
                ba_iterator = BA.objects.get(year=rea.ba.year, type="CA")
                ba_iterator.iterator = ba_iterator.iterator + 1
                rea.ba_id = ba_iterator.iterator
                ba_iterator.save()
            else:
                ba_iterator = BA(type="CA", year=rea.ba.year, iterator=0)
                rea.ba_id = ba_iterator.iterator
                ba_iterator.save()
        rea.save()
        try:
            realisateur = Realisateur.objects.get(member=rea.id)
            # Champs à synchroniser
            for field in ['ba', 'ba_id']:
                setattr(realisateur, field, getattr(rea, field))
            realisateur.save()
        except Realisateur.DoesNotExist:
            pass  # Pas de mission liée, on ne fait rien

        monsieurmadame = 'Monsieur' if rea.gender == 'M.' else 'Madame'
        ref = 'BA_'+str(rea.ba.year % 100)+'_C' + '%03d' % rea.ba_id
        return computeDocx({'ba': {'etudiant': rea, 'ref': ref.upper(), 'monsieurmadame': monsieurmadame}}, 'BA.docx', 'BA-' + ref)


class BAReaView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        'GET': ['ROLE_CA']
    }

    def retrieve(request, self, etudiant_id):
        rea = Realisateur.objects.get(pk=etudiant_id)
        if rea.ba == None:
            rea.ba = date.today()
            if BA.objects.filter(year=rea.ba.year, type="REA").first():
                ba_iterator = BA.objects.get(year=rea.ba.year, type="REA")
                ba_iterator.iterator = ba_iterator.iterator + 1
                rea.ba_id = ba_iterator.iterator
                ba_iterator.save()
            else:
                ba_iterator = BA(type="REA", year=rea.ba.year, iterator=0)
                rea.ba_id = ba_iterator.iterator
                ba_iterator.save()
        rea.save()
        monsieurmadame = 'Monsieur' if rea.gender == 'M.' else 'Madame'
        ref = 'BA_'+str(rea.ba.year % 100)+'_R' + '%03d' % rea.ba_id
        return computeDocx({'ba': {'etudiant': rea, 'ref': ref.upper(), 'monsieurmadame': monsieurmadame}}, 'BA.docx', 'BA-' + ref)


class FactureView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        # from modules/etudes/components/Generation.vue in modules/etudes/views/EtudeDetails.vue
        'GET': ['ROLE_CA']
    }

    def retrieve(request, self, facture_id):
        invoice = Facture.objects.get(pk=facture_id)
        return computeDocx({'facture': invoice}, 'FA.docx', str(invoice))

class SharedFactureView(generics.RetrieveAPIView):
    permission_classes = []
    required_groups = {
        # from modules/etudes/components/Generation.vue in modules/etudes/views/EtudeDetails.vue
        'GET': []
    }

    def retrieve(request, self, facture_id, key):
        signer = Signer()
        expected_key = signer.sign('facture'+str(facture_id))
        if(key == expected_key):
            invoice = Facture.objects.get(pk=facture_id)
            return computeDocx({'facture': invoice}, 'FA.docx', str(invoice))
        else:
            return HttpResponse("Invalid signature", status=HTTPStatus.FORBIDDEN)
        


class PVRView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        # from modules/etudes/components/Generation.vue in modules/etudes/views/EtudeDetails.vue
        'GET': ['ROLE_CA']
    }

    def retrieve(request, self, pvr_id):
        pvr = PVR.objects.get(pk=pvr_id)
        return computeDocx({'pvr': pvr}, 'PVR.docx')
