---
layout: default
title: Publications
permalink: /publications/
---

<div class="card">
  <h1 class="page-title">Publications</h1>

  {% assign pubs = site.data.publications %}

  {% assign years = pubs | map: "year" | uniq %}
  {% for y in years %}
    <h2 class="section-title">{{ y }}</h2>
    <div class="pub-list">
      {% for p in pubs %}
        {% if p.year == y %}
          <div class="pub-item">
            <div class="pub-title">{{ p.title }}</div>
            {% if p.authors and p.authors.size > 0 %}
              <div class="pub-authors">{{ p.authors | join: ", " }}</div>
            {% endif %}
            <div class="pub-venue">
              {% if p.venue != "" %}<span class="pub-venue-name">{{ p.venue }}</span>{% endif %}
              {% if p.volume != "" %}<span class="pub-meta"> {{ p.volume }}</span>{% endif %}
              {% if p.number != "" %}<span class="pub-meta">({{ p.number }})</span>{% endif %}
              {% if p.pages != "" %}<span class="pub-meta">: {{ p.pages }}</span>{% endif %}
            </div>
            <div class="pub-links">
              {% if p.doi != "" %}
                <a class="btn btn-sm" href="https://doi.org/{{ p.doi }}">DOI</a>
              {% endif %}
              {% if p.url != "" %}
                <a class="btn btn-sm" href="{{ p.url }}">Link</a>
              {% endif %}
            </div>
          </div>
        {% endif %}
      {% endfor %}
    </div>
  {% endfor %}
</div>
