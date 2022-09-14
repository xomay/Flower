from rest_framework.permissions import IsAuthenticated
from rest_framework import generics

from flower_app.controllers.permissions import HasGroupPermission
from .publishing import computeDocx
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


class CEView(generics.RetrieveAPIView):
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
        print(etude.contractType)
        if(etude.contractType=='CCA'):
            return computeDocx({'etude': etude}, 'CCA.docx', 'CCA-' + etude.name, images=images)
        elif(etude.contractType=='BC'):
            return computeDocx({'etude': etude}, 'BC.docx', 'BC-' + etude.name, images=images)
        else:
            return computeDocx({'etude': etude}, 'CETUDE.docx', 'CE-' + etude.name, images=images)


class RDMView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated, HasGroupPermission]
    required_groups = {
        # from modules/etudes/components/Generation.vue in modules/etudes/views/EtudeDetails.vue
        'GET': ['ROLE_CA']
    }

    def retrieve(request, self, rdm_id):
        mission = Mission.objects.get(pk=rdm_id)
        rea =mission.consultant
        if rea.ba != None:
            ref = 'RM_'+str(rea.ba.year % 100)+'C' + '%03d' % rea.ba_id+'_'+str(mission.project.number)
            return computeDocx({'rdm':{'mission': mission,'ref':ref}}, 'RDM.docx', 'RDM-' + mission.project.name)
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
