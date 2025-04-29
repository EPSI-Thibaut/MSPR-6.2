Collecte des informations sur l’espace de travail# Documentation Technique : Solution ETL pour l'Analyse des Données de Pandémies

## Introduction

Cette documentation présente la solution ETL (Extract, Transform, Load) mise en place dans le cadre du projet de détection et prévention des pandémies pour l'OMS. Cette solution permet d'extraire des données de pandémies depuis des fichiers CSV, de les normaliser et de les charger dans une base de données relationnelle pour permettre leur analyse comparative.

## 1. Extraction des Données (Extract)

### 1.1 Sources de Données
Le système extrait les données à partir de trois fichiers CSV distincts :
- **Données SARS** : `sars_2003_complete_dataset_clean.csv`
- **Données COVID (résumé)** : `worldometer_coronavirus_summary_data.csv`
- **Données COVID (quotidien)** : `worldometer_coronavirus_daily_data.csv`

### 1.2 Processus d'Extraction

L'extraction est réalisée par la classe `ReadToCsv` qui utilise la bibliothèque OpenCSV pour convertir les données CSV en objets Java :

```java
public List<SarsDto> readSarsData(String path) throws IOException {
    // Vérification et affichage des en-têtes du fichier
    displayCsvHeaders(path, "SARS");

    try (FileReader reader = new FileReader(path)) {
        // Configuration de la stratégie de mapping
        HeaderColumnNameMappingStrategy<SarsDto> strategy = new HeaderColumnNameMappingStrategy<>();
        strategy.setType(SarsDto.class);
        
        // Parse le fichier CSV en liste d'objets SarsDto
        List<SarsDto> data = new CsvToBeanBuilder<SarsDto>(reader)
                .withMappingStrategy(strategy)
                .withSeparator(',')
                .build()
                .parse();

        // Validation des données
        List<SarsDto> validData = data.stream()
                .filter(dto -> dto.getCountry() != null && !dto.getCountry().isEmpty())
                .collect(Collectors.toList());
        
        // Journalisation des statistiques d'extraction
        System.out.println("Total des enregistrements SARS lus: " + data.size());
        System.out.println("Enregistrements SARS valides: " + validData.size());
        
        return validData;
    } catch (Exception e) {
        // Gestion des erreurs
        throw new IOException("Échec du parsing des données SARS", e);
    }
}
```

Des méthodes similaires existent pour l'extraction des données COVID (`readCovidData`) et COVID quotidiennes (`readCovidDailyData`).

### 1.3 Validation des Fichiers

Avant toute extraction, la méthode `verifyFile` est utilisée pour vérifier l'existence et la lisibilité des fichiers :

```java
private static void verifyFile(Path filePath) {
    File file = filePath.toFile();
    System.out.println("\nVérification du fichier: " + filePath.toAbsolutePath());
    System.out.println("Le fichier existe: " + file.exists());
    System.out.println("Le fichier est lisible: " + file.canRead());
    System.out.println("Taille du fichier: " + file.length() + " octets");
}
```

### 1.4 Affichage des En-têtes CSV

Pour faciliter le débogage, la méthode `displayCsvHeaders` affiche les en-têtes CSV au début de chaque processus d'extraction :

```java
private void displayCsvHeaders(String path, String fileType) throws IOException {
    // Code pour afficher les en-têtes CSV
}
```

## 2. Transformation des Données (Transform)

La transformation des données est gérée principalement par la classe `DataNormalizationService`, qui offre diverses méthodes de normalisation et de nettoyage.

### 2.1 Normalisation des Noms de Pays

Pour assurer la cohérence entre les différentes sources de données, les noms de pays sont normalisés :

```java
private static final Map<String, String> COUNTRY_NAME_MAPPING = new HashMap<>();

static {
    COUNTRY_NAME_MAPPING.put("US", "United States");
    COUNTRY_NAME_MAPPING.put("USA", "United States");
    COUNTRY_NAME_MAPPING.put("United States of America", "United States");
    COUNTRY_NAME_MAPPING.put("UK", "United Kingdom");
    COUNTRY_NAME_MAPPING.put("UAE", "United Arab Emirates");
    COUNTRY_NAME_MAPPING.put("South Korea", "Korea, South");
}

public static String normalizeCountryName(String countryName) {
    if (countryName == null || countryName.trim().isEmpty()) {
        return null;
    }
    
    String trimmed = countryName.trim();
    return COUNTRY_NAME_MAPPING.getOrDefault(trimmed, trimmed);
}
```

### 2.2 Validation des Continents

Les continents sont également validés pour assurer l'intégrité des données :

```java
private static final Set<String> VALID_CONTINENTS = new HashSet<>();

static {
    VALID_CONTINENTS.add("Africa");
    VALID_CONTINENTS.add("Asia");
    VALID_CONTINENTS.add("Europe");
    VALID_CONTINENTS.add("North America");
    VALID_CONTINENTS.add("South America");
    VALID_CONTINENTS.add("Oceania");
    VALID_CONTINENTS.add("Antarctica");
}

public static boolean isValidContinent(String continent) {
    return continent != null && VALID_CONTINENTS.contains(continent.trim());
}
```

### 2.3 Identification du Type de Pandémie

Le système identifie automatiquement le type de pandémie en fonction du nom de fichier :

```java
public static String determinePandemicType(String fileName) {
    if (fileName == null) {
        return PANDEMIC_COVID; // Par défaut
    }
    
    String lowerCase = fileName.toLowerCase();
    if (lowerCase.contains("sars")) {
        return PANDEMIC_SARS;
    } else {
        return PANDEMIC_COVID;
    }
}
```

### 2.4 Filtrage des Données Invalides

Les données sont filtrées pour éliminer les entrées non valides :

```java
List<SarsDto> validData = data.stream()
        .filter(dto -> dto.getCountry() != null && !dto.getCountry().isEmpty())
        .collect(Collectors.toList());
```

### 2.5 Gestion des Valeurs Nulles

Les valeurs nulles sont gérées pour éviter les erreurs d'insertion :

```java
if (dto.getCumulativeTotalCases() != null) {
    totalByDay.setCaseCount(dto.getCumulativeTotalCases().intValue());
} else {
    totalByDay.setCaseCount(0);
}
```

### 2.6 Tri des Données

Les données sont triées par date pour assurer une cohérence chronologique :

```java
List<SarsDto> sortedData = sarsData.stream()
        .sorted(Comparator.comparing(SarsDto::getDate))
        .collect(Collectors.toList());
```

## 3. Chargement des Données (Load)

Le chargement des données transformées dans la base de données est géré par la classe `DataInsertionService`.

### 3.1 Séquence de Chargement des Données

La séquence d'insertion des données est cruciale pour maintenir l'intégrité référentielle :

1. **Extraction des relations continent-pays** : `extractContinentData()`
2. **Création des continents** : `createContinents()`
3. **Initialisation des pandémies** : `initializeDatabase()`
4. **Préparation des régions** : `prepareRegions()`
5. **Insertion des données SARS** : `insertSarsData()`
6. **Insertion des données COVID quotidiennes** : `insertCovidDailyData()`
7. **Création des associations pays-continents** : `createCountriesWithContinents()`

### 3.2 Initialisation des Pandémies

```java
@Transactional
public void initializeDatabase() {
    // Créer les deux types de pandémies (SARS et COVID-19)
    Pandemics sarsPandemic = createPandemic(DataNormalizationService.PANDEMIC_SARS);
    Pandemics covidPandemic = createPandemic(DataNormalizationService.PANDEMIC_COVID);
    
    // Journalisation des pandémies créées
    System.out.println("Pandémie SARS créée avec ID: " + sarsPandemic.getIdPandemics() + 
                       " et nom: " + sarsPandemic.getName());
    System.out.println("Pandémie COVID créée avec ID: " + covidPandemic.getIdPandemics() + 
                       " et nom: " + covidPandemic.getName());
}
```

### 3.3 Création des Continents

```java
@Transactional
public void createContinents(List<CovidDto> covidData) {
    // Extraction des noms de continents uniques
    Set<String> continents = countryToContinentMap.values().stream()
            .filter(c -> c != null && !c.trim().isEmpty())
            .collect(Collectors.toSet());

    // Création ou récupération de chaque continent
    for (String continentName : continents) {
        Continents continent = continentsRepository.findByName(continentName);
        
        if (continent == null) {
            continent = new Continents();
            continent.setName(continentName);
            continent = continentsRepository.save(continent);
        }
        
        continentsMap.put(continentName, continent);
    }
}
```

### 3.4 Préparation des Régions (Pays)

```java
@Transactional
public void prepareRegions(List<SarsDto> sarsData, List<CovidDto> covidData, List<CovidDailyDto> covidDailyData) {
    // Création des régions à partir des données SARS
    if (sarsData != null) {
        for (SarsDto dto : sarsData) {
            if (dto.getCountry() != null) {
                createRegion(dto.getCountry());
            }
        }
    }

    // Création des régions à partir des données COVID
    // Code similaire pour covidData et covidDailyData
}
```

### 3.5 Insertion des Données SARS et COVID

```java
@Transactional
public void insertSarsData(List<SarsDto> sarsData) {
    // Récupération de la référence à la pandémie SARS
    Pandemics sarsPandemic = pandemicsMap.get(DataNormalizationService.PANDEMIC_SARS);

    // Tri des données par date
    List<SarsDto> sortedData = sarsData.stream()
            .sorted(Comparator.comparing(SarsDto::getDate))
            .collect(Collectors.toList());

    // Traitement de chaque enregistrement
    for (SarsDto dto : sortedData) {
        // Normalisation du nom de pays
        String normalizedCountry = DataNormalizationService.normalizeCountryName(dto.getCountry());
        Regions region = regionsMap.get(normalizedCountry);

        // Création de l'objet TotalByDay et insertion en base
        if (region != null) {
            try {
                TotalByDay totalByDay = new TotalByDay();
                totalByDay.setId(new TotalByDayId(sarsPandemic.getIdPandemics(),
                        region.getIdRegions(),
                        new Date(dto.getDate().getTime())));

                totalByDay.setCaseCount(dto.getTotalCases());
                totalByDay.setDeath(dto.getDeaths());
                totalByDay.setRecovered(dto.getRecovered());
                totalByDay.setPandemics(sarsPandemic);
                totalByDay.setRegions(region);

                totalByDayRepository.save(totalByDay);
            } catch (Exception e) {
                // Gestion des erreurs d'insertion
            }
        }
    }
}
```

Une méthode similaire `insertCovidDailyData` existe pour les données COVID quotidiennes.

### 3.6 Création des Relations Continent-Pays pour le Frontend

```java
@Transactional
public void createCountriesWithContinents() {
    // Parcours des associations pays-continent
    for (Map.Entry<String, String> entry : countryToContinentMap.entrySet()) {
        String countryName = entry.getKey();
        String continentName = entry.getValue();

        // Récupération du continent
        if (continentName != null && continentsMap.containsKey(continentName)) {
            Continents continent = continentsMap.get(continentName);

            // Création ou mise à jour du pays
            Countries country = countriesRepository.findByName(countryName);
            if (country == null) {
                country = new Countries();
                country.setName(countryName);
                country.setContinents(continent);
                countriesRepository.save(country);
            } else if (country.getContinents() == null) {
                country.setContinents(continent);
                countriesRepository.save(country);
            }
        }
    }
}
```

## 4. Schéma Global du Processus ETL

```
+----------------+      +--------------------+      +----------------+
|  Extraction    |      |  Transformation    |      |   Chargement   |
|                |      |                    |      |                |
| * readSarsData |----->| * normalizeCountry |----->| * createCont.  |
| * readCovidData|      | * filterInvalid    |      | * prepareRegions|
| * readDaily    |      | * sortByDate       |      | * insertData   |
+----------------+      +--------------------+      +----------------+
```

## 5. Points Forts et Avantages de la Solution ETL

1. **Architecture modulaire** : Séparation claire des responsabilités entre extraction, transformation et chargement
2. **Traçabilité complète** : Journalisation détaillée de chaque étape du processus
3. **Gestion des erreurs robuste** : Traitement des exceptions à chaque niveau
4. **Normalisation des données** : Uniformisation des noms de pays et validation des continents
5. **Transactionnalité** : Utilisation des transactions Spring pour assurer l'intégrité des données
6. **Support pour plusieurs sources** : Capacité à intégrer des données de différentes pandémies

## 6. Conclusion

La solution ETL mise en place permet d'extraire efficacement les données de pandémies à partir de fichiers CSV, de les normaliser pour assurer leur cohérence et de les charger dans une base de données structurée pour l'analyse.