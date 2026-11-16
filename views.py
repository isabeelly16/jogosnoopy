
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from django.db.models import Max
from .models import Jogador, Pontuacao

@require_GET
def status(request):
    return JsonResponse({"online": True, "servico": "Ranking Snoopy"})

@csrf_exempt
@require_POST
def salvar_pontuacao(request):
    try:
        dados = json.loads(request.body.decode("utf-8"))
        nome = str(dados.get("jogador", "")).strip()[:30]
        pontos = int(dados.get("pontuacao", 0))
        fase = int(dados.get("fase", 1))
        pistas = int(dados.get("pistas", 0))
        if not nome:
            return JsonResponse({"erro": "Informe o nome do jogador."}, status=400)
        if pontos < 0 or not 1 <= fase <= 8 or pistas < 0:
            return JsonResponse({"erro": "Dados de pontuação inválidos."}, status=400)
        jogador, _ = Jogador.objects.get_or_create(nome=nome)
        Pontuacao.objects.create(
            jogador=jogador, pontuacao=pontos, fase=fase, pistas=pistas
        )
        return JsonResponse({"ok": True, "mensagem": "Pontuação salva no ranking online!"})
    except (ValueError, TypeError, json.JSONDecodeError):
        return JsonResponse({"erro": "Não foi possível interpretar os dados."}, status=400)

@require_GET
def ranking(request):
    melhores = (
        Pontuacao.objects.values("jogador__nome")
        .annotate(melhor_pontuacao=Max("pontuacao"))
        .order_by("-melhor_pontuacao", "jogador__nome")[:10]
    )
    resultado = []
    for item in melhores:
        registro = Pontuacao.objects.filter(
            jogador__nome=item["jogador__nome"],
            pontuacao=item["melhor_pontuacao"]
        ).order_by("-data").first()
        resultado.append({
            "jogador": item["jogador__nome"],
            "pontuacao": item["melhor_pontuacao"],
            "fase": registro.fase if registro else 1,
            "pistas": registro.pistas if registro else 0,
            "data": registro.data.isoformat() if registro else None,
        })
    return JsonResponse({"ranking": resultado})
