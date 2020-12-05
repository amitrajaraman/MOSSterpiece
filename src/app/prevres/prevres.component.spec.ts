import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PrevresComponent } from './prevres.component';

describe('PrevresComponent', () => {
  let component: PrevresComponent;
  let fixture: ComponentFixture<PrevresComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PrevresComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PrevresComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
