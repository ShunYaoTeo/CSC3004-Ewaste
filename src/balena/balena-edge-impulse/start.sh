#!/bin/sh

# EI_API_KEY defined as environment variables in BalenaCloud

# Fill out and uncomment for local deployment
#EI_API_KEY="ei_d11156e5320e250d938808c9b93c44caafbe76ba69b3575d" V1
#EI_API_KEY="ei_4b6f625790184982ad8862cfcfd37de18d8851f9124a771d"
#EI_COLLECT_MODE=0
#EI_COLLECT_MODE=1 0 when done collecting

if [ $EI_COLLECT_MODE = "1" ];
then
    edge-impulse-linux --api-key $EI_API_KEY --disable-microphone
else
    edge-impulse-linux-runner --api-key $EI_API_KEY --disable-microphone
fi