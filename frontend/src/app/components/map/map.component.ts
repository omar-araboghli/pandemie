import { Component, OnInit } from '@angular/core';
import { PlatformLocation } from '@angular/common'
import { MapService } from '../../services/map/map.service';

let mapboxgl = require('mapbox-gl/dist/mapbox-gl.js');
mapboxgl.accessToken = 'pk.eyJ1IjoicHVibGljLWRvbWFpbi1uYW1lIiwiYSI6ImNrNTk2Ynl1cTBpazkzZHJmcG9rMndvYmYifQ.hvQw7nr0wtZeUbSOuSU5CQ';


@Component({
  selector: 'app-map',
  templateUrl: './map.component.html',
  styleUrls: ['./map.component.css']
})
export class MapComponent implements OnInit {
  request: any
  msg: string
  gameEnded: boolean = false;

  constructor(private mapService: MapService, location: PlatformLocation) {
    location.onPopState(() => {

      this.endGame();

    });
   }

  ngOnInit() {
    var map = new mapboxgl.Map({
      container: 'map',
      style: 'mapbox://styles/aoomar33/ck47etxq82v6i1cowdwg6gxlq',
      center: [-10.5, 50],
      zoom: 1 // starting zoom
      });
      this.load(map);
  }

  private load(map){
    this.getFrontend();

    let infectedCities = this.getInfectedCities();
    let gameState = this.getGameState();
    let context = this; 

    map.on('load', function() {
      map.loadImage(
        '../../assets/dot.jpg',
          async function(error, image) {
            if (error) throw error;
              map.addImage('dot', image);

              context.addInfectedCitiesLayer(map, infectedCities);
              context.addRoundLayer(map, gameState);
            
            while (context.isPending() && !context.gameEnded) {
              await context.getFrontend();
              infectedCities = context.getInfectedCities();
              gameState = context.getGameState();

              let dots = { type: 'FeatureCollection', features: infectedCities };
              map.getSource('points').setData(dots);

              let state = {type: 'FeatureCollection', features: gameState['data'].features}
              map.getSource('state').setData(state);
            }
            
          }
      );
    });
  }

  private addInfectedCitiesLayer(map, infectedCities){
    let dots = { type: 'geojson', data: { type: 'FeatureCollection', features: infectedCities }};
              
    map.addLayer({
          'id': 'points',
          'source': dots,
          'type': 'symbol',
          'layout': {
              'icon-image': 'dot',
              'icon-size': 0.02
              }
    });
  }

  private addRoundLayer(map, gameState) {
    
   map.addLayer({
     'id': 'state',
         'source': gameState,
         'type': 'symbol',
         'layout': {
           'text-field': ['get', 'description'],
           'text-variable-anchor': ['top', 'bottom', 'left', 'right'],
           'text-radial-offset': 0.5,
           'text-justify': 'auto',
           }
   });
  }

  private isPending() {
    if (!this.request) {
      return true;
    }
    return this.request.outcome === 'pending';
  }

  private getGameState(){
    let info = 'Round: \nOutcome: \nPoints: \nAction: ';

    if (this.request) {
      info = 'Round: ' + this.request.round + '\nOutcome: ' + this.request.outcome
              + '\nPoints: ' + this.request.points + '\nAction: ' + this.request.action;
    }

    let gameState = {
      'type': 'geojson',
     'data':
         { 
           'type': 'FeatureCollection',
           'features': [ 
             {
             'type': 'Feature',
             'properties': {
                 'description': info,
               },
             'geometry': {
                  'type': 'Point',
                   'coordinates': [-173, 77]
                 } 
             }
           ]
          }
         };
    return gameState
  }

  private getInfectedCities(){
    if (!this.request || !this.request.hasOwnProperty('cities')) {
      return [];
    }

    let features = [];
    let context = this;
    Object.keys(context.request.cities).forEach(function(i) {
      if (context.hasPathogen(context.request.cities[i])) {
        features.push(
          {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [context.request.cities[i].longitude, context.request.cities[i].latitude]
            }
          }
        );
      }
    });
    return features;
  }

  private hasPathogen(city: any) {
    let flag = false;
    if (city.hasOwnProperty('events')) {
      Object.keys(city.events).forEach(function(i) {
        if (city.events[i].type === 'pathogenEncountered' || 
            city.events[i].type === 'bioTerrorism' ||
            city.events[i].type === 'outbreak'){
              flag = true;
            }
      });
    }
    return flag;
  }

  private async getFrontend() {
    await this.mapService.getFrontend()
      .subscribe((request: any) => {
        this.request = request;
        console.log(this.request);
        }
      );
      await this.mapService.delay(3000);
  }

  public endGame() {
    this.mapService.endGame()
      .subscribe((res: any) => {
        this.msg = 'Game ' + res['Game'];
        console.log(res);
        }
      );
    this.gameEnded = true;
  }
}
