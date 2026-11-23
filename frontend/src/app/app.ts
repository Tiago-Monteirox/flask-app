import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Component, OnInit, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { finalize } from 'rxjs';

interface Event {
  id: number;
  title: string;
  date: string;
}

interface EventPayload {
  title: string;
  date: string;
}

@Component({
  selector: 'app-root',
  imports: [FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css',
})
export class App implements OnInit {
  private readonly http = inject(HttpClient);
  private readonly apiUrl = '/events';

  events = signal<Event[]>([]);
  form: EventPayload = { title: '', date: '' };
  searchId: number | null = null;
  searchedEvent = signal<Event | null>(null);
  editingId = signal<number | null>(null);
  loading = signal(true);
  searching = signal(false);
  saving = signal(false);
  errorMessage = signal('');
  searchError = signal('');
  successMessage = signal('');

  ngOnInit(): void {
    this.loadEvents();
  }

  loadEvents(showConfirmation = false): void {
    this.loading.set(true);
    this.errorMessage.set('');

    this.http
      .get<Event[]>(this.apiUrl)
      .pipe(finalize(() => this.loading.set(false)))
      .subscribe({
        next: (events) => {
          this.events.set(this.sortEvents(events));

          if (showConfirmation) {
            this.successMessage.set('GET /events executado com sucesso.');
          }
        },
        error: (error) => this.errorMessage.set(this.getErrorMessage(error)),
      });
  }

  searchEventById(): void {
    const eventId = Number(this.searchId);

    this.searchedEvent.set(null);
    this.searchError.set('');

    if (!Number.isInteger(eventId) || eventId <= 0) {
      this.searchError.set('Informe um ID inteiro maior que zero.');
      return;
    }

    this.searching.set(true);

    this.http
      .get<Event>(`${this.apiUrl}/${eventId}`)
      .pipe(finalize(() => this.searching.set(false)))
      .subscribe({
        next: (event) => this.searchedEvent.set(event),
        error: (error) => this.searchError.set(this.getErrorMessage(error)),
      });
  }

  saveEvent(): void {
    const payload: EventPayload = {
      title: this.form.title.trim(),
      date: this.form.date,
    };

    if (!payload.title || !payload.date) {
      this.errorMessage.set('Preencha o título e a data.');
      return;
    }

    this.saving.set(true);
    this.errorMessage.set('');
    this.successMessage.set('');

    const editingId = this.editingId();
    const request = editingId === null
      ? this.http.post<Event>(this.apiUrl, payload)
      : this.http.put<Event>(`${this.apiUrl}/${editingId}`, payload);

    request
      .pipe(finalize(() => this.saving.set(false)))
      .subscribe({
        next: () => {
          this.successMessage.set(editingId === null
            ? 'Evento criado com sucesso.'
            : 'Evento atualizado com sucesso.');
          this.resetForm();
          this.loadEvents();
        },
        error: (error) => this.errorMessage.set(this.getErrorMessage(error)),
      });
  }

  editEvent(event: Event): void {
    this.errorMessage.set('');
    this.successMessage.set('');

    this.http.get<Event>(`${this.apiUrl}/${event.id}`).subscribe({
      next: (selectedEvent) => {
        this.editingId.set(selectedEvent.id);
        this.form = { title: selectedEvent.title, date: selectedEvent.date };
        window.scrollTo({ top: 0, behavior: 'smooth' });
      },
      error: (error) => this.errorMessage.set(this.getErrorMessage(error)),
    });
  }

  cancelEdit(): void {
    this.resetForm();
  }

  deleteEvent(event: Event): void {
    if (!window.confirm(`Remover o evento "${event.title}"?`)) {
      return;
    }

    this.errorMessage.set('');
    this.successMessage.set('');

    this.http.delete<{ message: string }>(`${this.apiUrl}/${event.id}`).subscribe({
      next: () => {
        this.events.update((events) => events.filter((item) => item.id !== event.id));
        this.successMessage.set('Evento removido com sucesso.');

        if (this.editingId() === event.id) {
          this.resetForm();
        }
      },
      error: (error) => this.errorMessage.set(this.getErrorMessage(error)),
    });
  }

  formatDate(date: string): string {
    const [year, month, day] = date.split('-');
    return `${day}/${month}/${year}`;
  }

  private resetForm(): void {
    this.form = { title: '', date: '' };
    this.editingId.set(null);
  }

  private sortEvents(events: Event[]): Event[] {
    return [...events].sort((first, second) => first.date.localeCompare(second.date));
  }

  private getErrorMessage(error: HttpErrorResponse): string {
    const apiMessage = error.error?.message;

    return typeof apiMessage === 'string'
      ? apiMessage
      : 'Não foi possível conectar à API Flask.';
  }
}
