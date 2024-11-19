# Assessment
## Aanpak en ontwerpkeuzes
### Model
Er is een eenvoudig model met een PointField, een DateTimeField, en een
ForeignKey naar een User.

### View
Ik koos voor een ModelViewSet van DJRF, omdat deze de mogelijkheid
heeft om zowel GET als POST routes te beschrijven.

De get_queryset bevat filters om de geo-punten te filteren op user:
- superusers zien alles
- gewone users zien hun eigen punten en punten zonder user
- anonieme users zien alleen punten zonder user

Daarnaast kan de gebruiker query parameters meegeven in de request
(lat, lon, distance), om te filteren op punten die binnen <distance>
meters van (lat,lon) liggen.

### Serializer
Ik heb een externe library gebruikt voor het omvormen van coordinaten
-strings naar een Point. Daarin zit al validatie voor het bestaan van
zowel een latitude als longitude.

Ik heb een validator functie toegevoegd om te checken of de coordinaten
binnen de normale grenzen vallen (default SRID 4326).

### Tests
Ik heb een aantal tests geschreven, maar kwam wat issues tegen bij het
schrijven van tests voor de API endpoints. Deze heb ik wel handmatig
getest maar de geautomatiseerde tests kreeg ik niet op tijd af.

## Configuratiebestand
_"Bedenk een methode om dynamisch views te maken op basis van datamodellen die door gebruikers worden aangeleverd (bijvoorbeeld via een configuratiebestand) Zodat voor elk model een eigen endpoint wordt gemaakt."_

Mijn aanpak hierin zou ongeveer als volgt zijn:
1. vaststellen van de vorm van het configuratiebestand (type velden,
structuur, etc.)
2. upload-functie implementeren waar de gebruiker het bestand kan
uploaden
3. validatie van het bestand op basis van de DSL van punt 1.
4. templates schrijven voor modelen op basis waarvan een nieuwe
django app kan worden gebouwd.
5. script schrijven wat deze templates gebruikt om de code op te
zetten, de migraties te bouwen en runnen, en te registreren zodat
django alles kan vinden.
6. script om een pull request te maken en iets als een github actie om
de boel te kunnen deployen (in ieder geval) op een staging server.
