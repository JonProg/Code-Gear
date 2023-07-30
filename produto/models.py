from django.template.loader import get_template
from django.db import models
from utils.images import resize_image
from utils.rands import slugify_new

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    imagem = models.ImageField(
        upload_to='produto_imagens/%Y/%m/'
    )
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco_marketing = models.FloatField(default=0)
    preco_marketing_promocional = models.FloatField(default=0)

    def img_preview(self): 
        return get_template('produto/img_preview.html').render({
        'field_name': 'imagem',
        'src': self.imagem.url if self.imagem else None,
        }
    )

    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variável'),
            ('S', 'Simples'),
        )
    )

    def get_preco_formatado(self):
        return f'R$ {self.preco_marketing:.2f}'.replace('.',',')
    get_preco_formatado.short_description = 'Preço'

    def get_preco_promocional(self):
        return f'R$ {self.preco_marketing_promocional:.2f}'.replace('.',',')
    get_preco_promocional.short_description = 'Preço Promo.'

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify_new(self.nome, 4)

        current_imagem_name = str(self.imagem.name)
        super_save = super().save(*args, **kwargs)
        imagem_changed = False

        if self.imagem:
            imagem_changed = current_imagem_name != self.imagem.name

        if imagem_changed:
            resize_image(self.imagem, 800, True, 70)

        return super_save
       
    def __str__(self) -> str:
        return self.nome

class Variacao(models.Model):
    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'

    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=50, blank=True, null=True)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)

    def __str__(self) -> str:
        return self.nome or self.produto.nome


    





