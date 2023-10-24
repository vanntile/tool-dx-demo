#!/bin/zsh

# Data

F="/tmp/response.txt"
COMMANDS=("read" "create" "get")
ACTIONS=("ACCEPT_SRC" "ACCEPT_DST" "BLOCK_SRC" "BLOCK_DST" "FORWARD")
PROTOCOLS=("tcp" "udp" "icmp")

# Helpers
function end_if_empty() {
  if [ "$1" = "" ]; then
    [ -n "$2" ] && echo "No $2 provided"
    echo "Exiting with no changes" && exit 0
  fi
}

function manage_response() {
  if [ "$1" != "200" ] && [ "$1" != "201" ]; then
    echo "Error status code: $1"
  fi

  gum style --foreground 4 "Response body"
  cat "$F" | jq 
  rm "$F"
}

# Running

[ "$ADDRESS" = "" ] && ADDRESS=$(gum input --placeholder "Provide address of the router to configure")
end_if_empty "$ADDRESS" "address"

echo -n "Will configure router at: " && gum style --underline --foreground 2 "$ADDRESS"

COMMAND=$(gum choose --header="Choose desired command" $COMMANDS)
end_if_empty "$COMMAND" "command"

if [ "$COMMAND" = "read" ]; then
  LIMIT=1000

  if $(gum confirm "Default limit is $LIMIT. Change limit?"); then
    LIMIT=$(gum input --placeholder "Insert positive number limit")
    if [[ "$LIMIT" =~ ^[0-9]+$ ]]; then
      echo "Querying first $LIMIT routes"
    else
      end_if_empty "" "valid limit"
    fi
  fi

  HTTP_RESPONSE=$(curl -s -o "$F" -w "%{http_code}" "$ADDRESS/routes?limit=$LIMIT")
  manage_response "$HTTP_RESPONSE"
elif [ "$COMMAND" = "create" ]; then
  ACTION=$(gum choose --header="Choose desired action" $ACTIONS)
  end_if_empty "$ACTION" "action"

  SOURCE=null
  SOURCE_PORT=null
  DESTINATION=null
  DESTINATION_PORT=null
  PROTOCOL=null

  if $(gum confirm "Choose optional protocol?"); then
    PROTOCOL=$(gum choose --header="Select protocol" $PROTOCOLS)
    PROTOCOL="\"$PROTOCOL\""
  fi

  if [ "$ACTION" = "ACCEPT_SRC" ] || [ "$ACTION" = "BLOCK_SRC" ]; then
    SOURCE=$(gum input --placeholder "IP network address (CIDR format)")
    end_if_empty "$SOURCE" "source address"
    SOURCE="\"$SOURCE\""
    if $(gum confirm "Use custom port?"); then
      SOURCE_PORT=$(gum input --header="Port value")
      end_if_empty "$SOURCE_PORT" "port"
    fi
  elif [ "$ACTION" = "ACCEPT_DST" ] || [ "$ACTION" = "BLOCK_DST" ]; then
    DESTINATION=$(gum input --placeholder "IP network address (CIDR format)")
    end_if_empty "$DESTINATION" "destination address"
    DESTINATION="\"$DESTINATION\""
    if $(gum confirm "Use custom port?"); then
      DESTINATION_PORT=$(gum input --header="Port value")
      end_if_empty "$DESTINATION_PORT" "port"
    fi
  else
    SOURCE=$(gum input --placeholder "Source IP network address (CIDR format)")
    end_if_empty "$SOURCE" "source address"
    SOURCE="\"$SOURCE\""
    if $(gum confirm "Use custom source port?"); then
      SOURCE_PORT=$(gum input --header="Port value")
      end_if_empty "$SOURCE_PORT" "port"
    fi
    DESTINATION=$(gum input --placeholder "Destination IP network address (CIDR format)")
    end_if_empty "$DESTINATION" "destination address"
    DESTINATION="\"$DESTINATION\""
    if $(gum confirm "Use custom destination port?"); then
      DESTINATION_PORT=$(gum input --header="Port value")
      end_if_empty "$DESTINATION_PORT" "port"
    fi
  fi

  # Format body
  BODY="{
    \"source\": $SOURCE,
    \"source_port\": $SOURCE_PORT,
    \"destination\": $DESTINATION,
    \"destination_port\": $DESTINATION_PORT,
    \"protocol\": $PROTOCOL,
    \"action\": \"$ACTION\"
  }"
  echo "Will send the following route:\n\n$(echo $BODY | jq)" | gum style --foreground 2 --border-foreground 2 \
    --border double --width 79 --padding "0 2"

  if $(gum confirm "Send route?"); then
    HTTP_RESPONSE=$(curl -s -o "$F" -w "%{http_code}" -H "Content-Type: application/json" -d "$BODY" "$ADDRESS/routes")
    manage_response "$HTTP_RESPONSE"
  fi
else
  ID=$(gum input --placeholder "Provide UUID")
  end_if_empty "$ID" "id"

  HTTP_RESPONSE=$(curl -s -o "$F" -w "%{http_code}" "$ADDRESS/routes/$ID")
  manage_response "$HTTP_RESPONSE"
fi
