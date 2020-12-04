import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewCurrComponent } from './view-curr.component';

describe('ViewCurrComponent', () => {
  let component: ViewCurrComponent;
  let fixture: ComponentFixture<ViewCurrComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ViewCurrComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ViewCurrComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
