import { Component, OnInit } from '@angular/core';
import { MainService } from '../../services/main/main.service';


@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {
  title = 'Pandemie!';
  msg = '';

  constructor(private mainService: MainService) { }

  ngOnInit() {
  }

  public async startGame() {
    this.mainService.startGame()
    .subscribe((data: any) =>
      this.msg = data
      );
  }
  
}
