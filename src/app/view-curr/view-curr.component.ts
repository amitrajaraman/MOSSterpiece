import { Component, OnInit } from '@angular/core';
import { MessengerService } from '../shared.service';

@Component({
  selector: 'app-view-curr',
  templateUrl: './view-curr.component.html',
  styleUrls: ['./view-curr.component.scss']
})
export class ViewCurrComponent implements OnInit {

  constructor(public messengerService: MessengerService) { }

  ngOnInit(): void {
  }

}
