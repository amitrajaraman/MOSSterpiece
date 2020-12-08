import { Component, OnInit } from '@angular/core';
import { MessengerService } from '../shared.service';

@Component({
  selector: 'app-prevres',
  templateUrl: './prevres.component.html',
  styleUrls: ['./prevres.component.scss']
})
export class PrevresComponent implements OnInit {

  constructor(public messengerService: MessengerService) { }

  ngOnInit(): void {
  }

}
