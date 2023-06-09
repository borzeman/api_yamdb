from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from artworks.models import Title
from users.models import CustomUser


class AuthorTextModel(models.Model):
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ('pub_date',)

    def str(self):
        return self.text


class Review(AuthorTextModel):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка',
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        default_related_name = 'reviews'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_author_title_in_review',
            ),
        ]


class Comment(AuthorTextModel):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Отзыв',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        default_related_name = 'comments'
