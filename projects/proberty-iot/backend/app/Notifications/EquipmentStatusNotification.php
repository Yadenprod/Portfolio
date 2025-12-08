<?php

namespace App\Notifications;

use Illuminate\Bus\Queueable;
use Illuminate\Notifications\Notification;
use Illuminate\Notifications\Messages\MailMessage;
use Illuminate\Notifications\Messages\SlackMessage;
use App\Models\Equipment;

class EquipmentStatusNotification extends Notification
{
    use Queueable;

    protected $equipment;
    protected $status;

    public function __construct(Equipment $equipment, $status)
    {
        $this->equipment = $equipment;
        $this->status = $status;
    }

    public function via($notifiable)
    {
        return ['mail', 'slack'];
    }

    public function toMail($notifiable)
    {
        $status = $this->status;
        $equipment = $this->equipment;

        return (new MailMessage)
            ->subject("Статус оборудования: {$equipment->name}")
            ->line("Статус оборудования: {$status['overall_health']}")
            ->line("Критические датчики:")
            ->line(json_encode($status['critical_sensors'], JSON_PRETTY_PRINT))
            ->action('Просмотр оборудования', url("/equipment/{$equipment->id}"));
    }

    public function toSlack($notifiable)
    {
        $status = $this->status;
        $equipment = $this->equipment;

        return (new SlackMessage)
            ->warning()
            ->content("⚠️ Статус оборудования: {$equipment->name}")
            ->attachment(function ($attachment) use ($status) {
                $attachment
                    ->title('Детали статуса')
                    ->fields([
                        'Общее состояние' => $status['overall_health'],
                        'Критические датчики' => count($status['critical_sensors'])
                    ]);
            });
    }

    public static function sendNotification(Equipment $equipment, $status)
    {
        $users = \App\Models\User::whereIn('role_id', [1, 2])->get(); // Уведомляем администраторов и инженеров

        foreach ($users as $user) {
            $user->notify(new self($equipment, $status));
        }
    }
}
