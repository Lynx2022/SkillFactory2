from django import template


register = template.Library()

# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def censor(value):
   bad_words = ['Хуй','хуй','Бля','бля','еба','Еба','пиз','Пиз','Хер','хер', 'хуе','Хуе']
   value_= value.split()
   result = []
   for a in value_:
      if a[:3] in bad_words:
         a = a[0] + "*"*len(a[1:])
         result.append(a)
      else:
          result.append(a)
   return " ".join(result)

