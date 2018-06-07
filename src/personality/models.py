from django.db import models


class PersonalityType(models.Model):
    name   = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class PersonalityQuestion(models.Model):
    question_text   = models.CharField(max_length=100)
    category        = models.ForeignKey(PersonalityType, on_delete=models.CASCADE)

    def __str__(self):
        return self.question_text


class TestQuestion(models.Model):
    question_text   = models.CharField(max_length=100)

    def __str__(self):
        return self.question_text
    
    class Meta:
        ordering = ['?']


class TestChoice(models.Model):
    choice_text = models.CharField(max_length=100)
    question    = models.ForeignKey(TestQuestion, on_delete=models.CASCADE)
    is_answer   = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text