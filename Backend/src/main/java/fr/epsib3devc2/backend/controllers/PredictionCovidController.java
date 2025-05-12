package fr.epsib3devc2.backend.controllers;

import fr.epsib3devc2.backend.bo.CovidPrediction;
import fr.epsib3devc2.backend.repositories.PredictionCovidRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

// Création route pour recuperer les données de prédictions Covid
@RestController
@RequestMapping("/api/predictions")
public class PredictionCovidController {

    @Autowired
    private PredictionCovidRepository predictionRepository;

    @GetMapping
    public List<CovidPrediction> getAllPredictions() {
        return predictionRepository.findAll();
    }
}