Написать ReactJS-friendly сериалайзер.
 
Для примера остановимся на моделях:

    Car (машина)
      uid
      color
      vendor
      model

    Component (комплектующая)
      uid
      car
      type
      id

    Trip (Поездка)
      car
      distance
      start
      end

    Car 1:M Component
    Car 1:M Trip

=======================================
 
При создании Trip, нужно иметь возможность сослаться на Car с помощью uid
 
Например:

    POST /api/trip/
    {
       "start": "START DATETIME HERE",
       "end": "END DATETIME HERE",
       "distance": 10, // metres
       "car": "CAR_UUID_HERE"
    }
 
При создании Component, нужно иметь возможность сослаться на Car с помощью uid
 
Например:

    POST /api/component/
    {
       "type": 0, // engine
       "id": "VIN807",
       "car": "CAR_UUID_HERE"
    }
 
При этом, в выдаче по GET /api/car/UID
мы получим:

    {
       "uuid": "POLL_UUID_HERE",
       "VIN": "VIN807", // engine id
       "haul": 100, // пробег
       "trips": [
         {
           "uid": "TRIP_UID_HERE",
           "distance": 10,
           "start": "START DATETIME HERE",
           "end": "END DATETIME HERE"
         },
         ...
         {}
       ],
       "components": [
         {
           "type": 0, // engine
           "id": "VIN807",
         },
         ...
         {}
       ]
    }
 
Прошу обратить внимание на наличие в объекте car полей "пробег" и "номер двигателя".
Неуточнённые в задании детали прошу выполнить на своё усмотрение, предлагая наиболее
оптимальное с точки зрения исполнителя решение.
 
Опционально:
поддержка depth в сериалайзере
 
Дополнительно обращаю ваше внимание на то, что сериалайзер для модели Component, как и для
модели Trip должен быть один, т.е. не допускается классический для DRF подход вида

    ComponentCreatingSerializer(...):
        uid = ...
     
    ComponentListSerializer(...):
        class Meta:
        fields = ('uid', 'type', 'id')
