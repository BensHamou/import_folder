from django.shortcuts import render
from account.models import *
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from account.views import admin_required
import uuid
from .forms import *
from .filters import *
from django.core.paginator import Paginator
from django.urls import reverse
from django.http import JsonResponse
from django.views.generic.edit import CreateView, UpdateView
from django_filters.views import FilterView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
from functools import wraps
from .utils import *
from django.core.mail import send_mail
from django.utils.html import format_html
from django.template.defaulttags import register
import openpyxl
import os
from pathlib import Path

@register.filter
def startwith(value, word):
    return str(value).startswith(word)

@register.filter
def is_login(messages):
    for message in messages:
        if str(message).startswith('LOGIN : '):
            return True
    return False

@register.filter
def loginerror(value, word):
    return str(value)[len(word):]

@register.filter
def startswith(value, arg):
    return value.startswith(arg)

def check_creator(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'id' in kwargs:
            rep_id = kwargs['id']
        elif 'pk' in kwargs:
            rep_id = kwargs['pk']
        report = Report.objects.get(id=rep_id)
        if report.creator != request.user and not request.user.is_admin:
            return render(request, '403.html', status=403)
        return view_func(request, *args, **kwargs)
    return wrapper

def check_creatorPImported(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        pimported_id = kwargs.get('pk')
        pimported = PImported.objects.get(id=pimported_id)
        if not ((pimported.report.state == 'Brouillon' and request.user == pimported.report.creator) or request.user.is_admin):
            return render(request, '403.html', status=403)
        return view_func(request, *args, **kwargs)
    return wrapper


# Emplacements
@login_required(login_url='login')
@admin_required
def listEmplacementView(request):
    emplacements = Emplacement.objects.all().order_by('id')
    filteredData = EmplacementFilter(request.GET, queryset=emplacements)
    emplacements = filteredData.qs
    page_size_param = request.GET.get('page_size')
    page_size = int(page_size_param) if page_size_param else 12   
    paginator = Paginator(emplacements, page_size)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = { 'page': page, 'filtredData': filteredData,  }
    return render(request, 'list_emplacements.html', context)

@login_required(login_url='login')
@admin_required
def deleteEmplacementView(request, id):
    emplacement = Emplacement.objects.get(id=id)
    emplacement.delete()
    cache_param = str(uuid.uuid4())
    url_path = reverse('emplacements')
    redirect_url = f'{url_path}?cache={cache_param}'
    return redirect(redirect_url)

@login_required(login_url='login')
@admin_required
def createEmplacementView(request):
    form = EmplacementForm()
    if request.method == 'POST':
        form = EmplacementForm(request.POST)
        if form.is_valid():
            form.save()
            cache_param = str(uuid.uuid4())
            url_path = reverse('emplacements')
            redirect_url = f'{url_path}?cache={cache_param}'
            return redirect(redirect_url)
    context = {'form': form}
    return render(request, 'emplacement_form.html', context)

@login_required(login_url='login')
@admin_required
def editEmplacementView(request, id):
    emplacement = Emplacement.objects.get(id=id)
    form = EmplacementForm(instance=emplacement)
    if request.method == 'POST':
        form = EmplacementForm(request.POST, instance=emplacement)
        if form.is_valid():
            form.save()
            cache_param = str(uuid.uuid4())
            url_path = reverse('emplacements')
            page = request.GET.get('page', '1')
            page_size = request.GET.get('page_size', '12')
            search = request.GET.get('search', '')
            redirect_url = f'{url_path}?cache={cache_param}&page={page}&page_size={page_size}&search={search}'
            return redirect(redirect_url)
    context = {'form': form, 'emplacement': emplacement}

    return render(request, 'emplacement_form.html', context)

# Transitor
@login_required(login_url='login')
@admin_required
def listTransitorView(request):
    transitors = Transitor.objects.all().order_by('id')
    filteredData = TransitorFilter(request.GET, queryset=transitors)
    transitors = filteredData.qs
    page_size_param = request.GET.get('page_size')
    page_size = int(page_size_param) if page_size_param else 12   
    paginator = Paginator(transitors, page_size)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = { 'page': page, 'filtredData': filteredData }
    return render(request, 'list_transitors.html', context)

@login_required(login_url='login')
@admin_required
def deleteTransitorView(request, id):
    transitor = Transitor.objects.get(id=id)
    transitor.delete()
    cache_param = str(uuid.uuid4())
    url_path = reverse('transitors')
    redirect_url = f'{url_path}?cache={cache_param}'
    return redirect(redirect_url)

@login_required(login_url='login')
@admin_required
def createTransitorView(request):
    form = TransitorForm()
    if request.method == 'POST':
        form = TransitorForm(request.POST)
        if form.is_valid():
            form.save()
            cache_param = str(uuid.uuid4())
            url_path = reverse('transitors')
            redirect_url = f'{url_path}?cache={cache_param}'
            return redirect(redirect_url)
    context = {'form': form}
    return render(request, 'transitor_form.html', context)

@login_required(login_url='login')
@admin_required
def editTransitorView(request, id):
    transitor = Transitor.objects.get(id=id)
    form = TransitorForm(instance=transitor)
    if request.method == 'POST':
        form = TransitorForm(request.POST, instance=transitor)
        if form.is_valid():
            form.save()
            cache_param = str(uuid.uuid4())
            url_path = reverse('transitors')
            page = request.GET.get('page', '1')
            page_size = request.GET.get('page_size', '12')
            search = request.GET.get('search', '')
            redirect_url = f'{url_path}?cache={cache_param}&page={page}&page_size={page_size}&search={search}'
            return redirect(redirect_url)
    context = {'form': form, 'transitor': transitor}

    return render(request, 'transitor_form.html', context)

# BUDGET_COST
@login_required(login_url='login')
@admin_required
def listBudgetCostView(request):
    budgets = BudgetCost.objects.all().order_by('id')
    filteredData = BudgetCostFilter(request.GET, queryset=budgets)
    budgets = filteredData.qs
    page_size_param = request.GET.get('page_size')
    page_size = int(page_size_param) if page_size_param else 12   
    paginator = Paginator(budgets, page_size)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    context = { 'page': page, 'filtredData': filteredData }
    return render(request, 'list_budgets.html', context)

@login_required(login_url='login')
@admin_required
def deleteBudgetCostView(request, id):
    budget = BudgetCost.objects.get(id=id)
    budget.delete()
    cache_param = str(uuid.uuid4())
    url_path = reverse('budgets')
    redirect_url = f'{url_path}?cache={cache_param}'
    return redirect(redirect_url)

@login_required(login_url='login')
@admin_required
def createBudgetCostView(request):
    form = BudgetCostForm()
    if request.method == 'POST':
        form = BudgetCostForm(request.POST)
        if form.is_valid():
            form.save()
            cache_param = str(uuid.uuid4())
            url_path = reverse('budgets')
            redirect_url = f'{url_path}?cache={cache_param}'
            return redirect(redirect_url)
    context = {'form': form}
    return render(request, 'budget_form.html', context)

@login_required(login_url='login')
@admin_required
def editBudgetCostView(request, id):
    budget = BudgetCost.objects.get(id=id)
    form = BudgetCostForm(instance=budget)
    if request.method == 'POST':
        form = BudgetCostForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            cache_param = str(uuid.uuid4())
            url_path = reverse('budgets')
            page = request.GET.get('page', '1')
            page_size = request.GET.get('page_size', '12')
            search = request.GET.get('search', '')
            redirect_url = f'{url_path}?cache={cache_param}&page={page}&page_size={page_size}&search={search}'
            return redirect(redirect_url)
    context = {'form': form, 'budget': budget}

    return render(request, 'budget_form.html', context)

#REPORTS

class CheckEditorMixin:
    def check_editor(self, report):
        if (report.creator != self.request.user or report.state != 'Brouillon') and not self.request.user.is_admin:
            return False
        return True

    def dispatch(self, request, *args, **kwargs):
        report = self.get_object()  
        if not self.check_editor(report):
            return render(request, '403.html', status=403)
        return super().dispatch(request, *args, **kwargs)
    
class CheckReportViewerMixin:
    def check_viewer(self, report):
        sites = self.request.user.sites.all()
        if report.site not in sites and self.request.user.is_admin:
            return False
        return True

    def dispatch(self, request, *args, **kwargs):
        report = self.get_object()  
        if not self.check_viewer(report):
            return render(request, '403.html', status=403)
        return super().dispatch(request, *args, **kwargs)

class ReportInline():
    form_class = ReportForm
    model = Report
    template_name = "report_form.html"    
    login_url = 'login'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['sites'] = self.request.user.sites.all()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        named_formsets = self.get_named_formsets()
        if not all((x.is_valid() for x in named_formsets.values())):
            return self.render_to_response(self.get_context_data(form=form))
        report = form.save(commit=False)
        if not report.state or report.state == 'Brouillon':
            report.state = 'Brouillon'
        
        if not report.id:
            report.creator = self.request.user
        
        report.save()
        new = True
        if self.object:
            new = False
        else:
            self.object = report

        for name, formset in named_formsets.items():
            formset_save_func = getattr(self, 'formset_{0}_valid'.format(name), None)
            if formset_save_func is not None:
                formset_save_func(formset)
            else:
                formset.save()

        if not new:
            cache_param = str(uuid.uuid4())
            url_path = reverse('view_report', args=[self.object.pk])
            redirect_url = f'{url_path}?cache={cache_param}'
            return redirect(redirect_url)
        return redirect('list_report')

    def formset_pimporteds_valid(self, formset):
        pimporteds = formset.save(commit=False)
        for obj in formset.deleted_objects:
            obj.delete()
        for pimported in pimporteds:
            pimported.report = self.object
            pimported.save()

class ReportCreate(LoginRequiredMixin, ReportInline, CreateView):

    def get_context_data(self, **kwargs):
        ctx = super(ReportCreate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        if self.request.method == "GET":
            return {'pimporteds': PImportedsFormSet(prefix='pimporteds')}
        else:
            return {'pimporteds': PImportedsFormSet(self.request.POST or None, prefix='pimporteds')}

class ReportUpdate(LoginRequiredMixin, CheckEditorMixin, ReportInline, UpdateView):

    def get_context_data(self, **kwargs):
        ctx = super(ReportUpdate, self).get_context_data(**kwargs)
        ctx['named_formsets'] = self.get_named_formsets()
        return ctx

    def get_named_formsets(self):
        return {
            'pimporteds': PImportedsFormSet(self.request.POST or None, instance=self.object, prefix='pimporteds'),
        }
    
class ReportDetail(LoginRequiredMixin, CheckReportViewerMixin, DetailView):
    model = Report
    template_name = 'report_details.html'
    context_object_name = 'report'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        fields = [field for field in self.model._meta.get_fields() if field.concrete]
        context['fields'] = fields
        return context

class ReportList(LoginRequiredMixin, FilterView):
    model = Report
    template_name = "list_reports.html"
    context_object_name = "reports"
    filterset_class = ReportFilter
    ordering = ['-date_created', '-date_in_stock']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        sites = self.request.user.sites.all()
        queryset = queryset.filter(site__in=sites)
        return queryset   

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        page_size_param = self.request.GET.get('page_size')
        page_size = int(page_size_param) if page_size_param else 12        
        paginator = Paginator(context['reports'], page_size)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page'] = page_obj
        return context

@login_required(login_url='login')
@check_creator
def delete_report(request, pk):
    try:
        report = Report.objects.get(id=pk)
    except Report.DoesNotExist:
        messages.success(request, 'Le rapport n\'existe pas')
        url_path = reverse('list_report')
        cache_param = str(uuid.uuid4())
        redirect_url = f'{url_path}?cache={cache_param}'
        return redirect(redirect_url)

    report.delete()
    messages.success(request, 'Rapport supprimé avec succès')
    url_path = reverse('list_report')
    cache_param = str(uuid.uuid4())
    redirect_url = f'{url_path}?cache={cache_param}'
    return redirect(redirect_url)

@login_required(login_url='login')
@check_creatorPImported
def delete_product(request, pk):
    try:
        pimported = PImported.objects.get(id=pk)
    except PImported.DoesNotExist:
        messages.success(request, 'Produit importé untrouvable')
        url_path = reverse('edit_report', args=[pimported.report.id])
        cache_param = str(uuid.uuid4())
        redirect_url = f'{url_path}?cache={cache_param}'
        return redirect(redirect_url)

    pimported.delete()
    messages.success(request, 'Produit importé supprimé avec successé')
    url_path = reverse('edit_report', args=[pimported.report.id])
    cache_param = str(uuid.uuid4())
    redirect_url = f'{url_path}?cache={cache_param}'
    return redirect(redirect_url)


@login_required(login_url='login')
@check_creator
def confirmReport(request, pk):
    try:
        report = Report.objects.get(id=pk)
    except Report.DoesNotExist:
        messages.success(request, 'Report Does not exit')
    
    if report.state != 'Confirmé':
        report.state = 'Confirmé'
        report.save()

    subject = f'Rapport de dossier d\'importation [{report.id}]'
    address = 'http://pumaimportation.grupopuma-dz.com/report/'
    message = f'''
            <p>Bonjour l'équipe,</p>
            <p>Un rapport a été créé par <b style="color: #002060">{report.creator.fullname}</b></p>
    '''
    
    for pimported in report.pimporteds():
        found = False
        new_cost = round(pimported.cost_u, 3)
        new_ref = pimported.report.ref_folder
        article = f'[{pimported.article_code}] {pimported.article_designation}'
        
        prev_importation = PImported.objects.exclude(id=pimported.id).filter(article_id=pimported.article_id).order_by('-report__date_calc_cost').first()
        budget_obj = BudgetCost.objects.filter(article_id=pimported.article_id).first()
        if not budget_obj:
            cb, tr= 'Budget non renseigné.', 0
        else:
            cb, tr = budget_obj.budget, round(budget_obj.budget / new_cost, 2)
        if prev_importation:
            found = True
            old_cost = round(prev_importation.cost_u, 3)
            old_ref = prev_importation.report.ref_folder
        else:
            script_dir = Path(__file__).parent.absolute()
            excel_file_path = os.path.join(script_dir, 'old_products.xlsx')
            workbook = openpyxl.load_workbook(excel_file_path)
            sheet = workbook.active
            old_cost, old_ref = 0, ''
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if row[0] == pimported.article_code:
                    old_cost, old_ref = row[3], row[4]
                    found = True
                    break
            workbook.close()
        if not found:
            old_cost, old_ref = 0, 'Non trouvé'
        message += getArticleTable(old_cost, new_cost, cb, tr, old_ref, new_ref, article)
        message += '<br>'
    message += f'''<p>Pour plus de détails, veuillez visiter <a href="{address}{report.id}/">{address}{report.id}/</a>.</p>'''
    formatHtml = format_html(message)

    if report.site.address:
        recipient_list = report.site.address.split('&')
    else:
        recipient_list = ['benshamou@gmail.com'] 

    messages.success(request, 'Rapport validé avec succès')
    send_mail(subject, "", 'Puma Dossier d\'Importation', recipient_list, html_message=formatHtml)
    url_path = reverse('view_report', args=[report.id])
    cache_param = str(uuid.uuid4())
    redirect_url = f'{url_path}?cache={cache_param}'
    return redirect(redirect_url)

def getArticleTable(old_cost, new_cost, cb, tr, old_ref, new_ref, article):
    colorE = round(old_cost / new_cost, 2) >= 1 and 'green' or 'red'
    colorR = tr >= 1 and 'green' or 'red'
    emojiE = '⬆️' if round(old_cost / new_cost, 2) >= 1 else '⬇️'
    emojiR = '⬆️' if tr >= 1 else '⬇️'
    if isinstance(cb, float):
        cb = f'{round(cb, 3):,.2f}'
    table = f'<br><p>Produit <b style="color: #002060">{article}:</b></p><br>'
    table += '<table style="border-collapse: collapse; text-align: center; width: 100%;">'
    table += '<thead><tr><th></th>'
    table += '<th style="color: white; background-color: #002060; border-bottom: 1px solid black;">Dernier Coût</th>'
    table += '<th style="color: white; background-color: #002060; border-bottom: 1px solid black;">Coût Actuel</th>'
    table += '<th style="color: white; background-color: #002060; border-bottom: 1px solid black;">Coût Budgetaire</th>'
    table += '<th style="color: white; background-color: #002060; border-bottom: 1px solid black;">Taux Evolution</th>'
    table += '<th style="color: white; background-color: #002060; border-bottom: 1px solid black;">Taux Réalisation</th>'
    table += '</tr></thead><tbody>'
    table += '<tr style="border-bottom: 1px solid black;"><td></td>'
    table += f'<td style="color: black; background-color: #f2f2f2; border-bottom: 1px solid black;">{round(old_cost, 3):,.2f}</td>'
    table += f'<td style="color: black; background-color: #f2f2f2; border-bottom: 1px solid black;">{round(new_cost, 3):,.2f}</td>'
    table += f'<td style="color: black; background-color: #f2f2f2; border-bottom: 1px solid black;">{cb}</td>'
    table += f'<td style="color: {colorE}; background-color: #f2f2f2; border-bottom: 1px solid black;"><b>{round(old_cost / new_cost, 2):,.2f}% {emojiE}</b></td>'
    table += f'<td style="color: {colorR}; background-color: #f2f2f2; border-bottom: 1px solid black;"><b>{tr}% {emojiR}</b></td>'
    table += '</tr>'
    table += '<tr><td style="color: white; background-color: #002060;">N° dossier</td>'
    table += f'<td style="color: black; background-color: #f2f2f2;">{old_ref}</td>'
    table += f'<td style="color: black; background-color: #f2f2f2;">{new_ref}</td>'
    table += '<td style="color: black; background-color: #f2f2f2;"></td><td style="color: black; background-color: #f2f2f2;"></td><td style="color: black; background-color: #f2f2f2;"></td></tr></tbody></table>'
    return table

@login_required(login_url='login')
@check_creator
def cancelReport(request, pk):
    try:
        report = Report.objects.get(id=pk)
    except Report.DoesNotExist:
        messages.success(request, 'Report Does not exit')
    
    if report.state != 'Annulé':
        report.state = 'Annulé'
        report.save()
    
    url_path = reverse('view_report', args=[report.id])
    cache_param = str(uuid.uuid4())
    redirect_url = f'{url_path}?cache={cache_param}'
    return redirect(redirect_url)

@login_required(login_url='users:login')
def live_search(request):
    search_for = request.GET.get('search_for', '')
    term = request.GET.get('search_term', '')
    if search_for == 'fournisseur':
        records = getFournisseurId(term)
        if len(records) > 0:
            return JsonResponse([{'id': obj[0], 'name': obj[1].replace("'","\\'")} for obj in records], safe=False)
        
    elif 'article_code' in search_for:
        records = getProductId(term)
        if len(records) > 0:
            return JsonResponse([{'id': obj[0], 'name': obj[1].replace("'","\\'"), 'code': obj[2]} for obj in records], safe=False)
        
    return JsonResponse([], safe=False)
