
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name="Jogador",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("nome", models.CharField(max_length=30, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Pontuacao",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("pontuacao", models.PositiveIntegerField(default=0)),
                ("fase", models.PositiveSmallIntegerField(default=1)),
                ("pistas", models.PositiveSmallIntegerField(default=0)),
                ("data", models.DateTimeField(auto_now_add=True)),
                ("jogador", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="pontuacoes", to="ranking.jogador")),
            ],
            options={"ordering": ["-pontuacao", "-data"]},
        ),
    ]
