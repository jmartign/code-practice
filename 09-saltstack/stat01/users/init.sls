{% for user, uid in pillar.get('users', {}).item() %}
{{user}}:
  user.present:
    - uid: {{uid}}
{% endfor %}

