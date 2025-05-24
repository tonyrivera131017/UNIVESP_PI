from django import forms

from .models import MercadoLivreAd, Produto


class ProdutoForm(forms.ModelForm):
    mlb_id_vinculado = forms.CharField(
        label="MLB ID Vinculado",
        required=False,  # Permite deixar o campo em branco para desvincular
        max_length=50,
        help_text="Deixe em branco para desvincular o anúncio existente ou se não houver anúncio.",
    )

    class Meta:
        model = Produto
        fields = ["nome", "quantidade", "preco", "mlb_id_vinculado"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Preenche o campo com o mlb_id do primeiro anúncio, se existir
            primeiro_anuncio = self.instance.anuncios.first()
            if primeiro_anuncio:
                self.fields["mlb_id_vinculado"].initial = primeiro_anuncio.mlb_id
            else:
                self.fields["mlb_id_vinculado"].initial = ""
        else:
            self.fields["mlb_id_vinculado"].initial = ""


class MercadoLivreAdForm(forms.ModelForm):
    class Meta:
        model = MercadoLivreAd
        fields = ["mlb_id"]
