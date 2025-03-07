import { BiInfoCircle } from "react-icons/bi"
import { Link } from "react-router-dom"
import { Link as RadixLink, Text } from "@radix-ui/themes"
import useChatSettings from "@/hooks/fetchers/useChatSettings"
import { CustomCallout } from "@/components/common/Callouts/CustomCallout"

const AINotEnabledCallout = () => {

    const { chatSettings } = useChatSettings()

    if (chatSettings?.enable_ai_integration === 1) {
        return null
    }

    return (
        <CustomCallout
            iconChildren={<BiInfoCircle size='18' />}
            rootProps={{ color: 'blue', variant: 'surface' }}
            textChildren={<Text>Chat AI is not enabled. Please enable it in <RadixLink asChild color='blue' underline='always'><Link to='/settings/openai-settings'>OpenAI Settings</Link></RadixLink></Text>}
        />
    )
}

export default AINotEnabledCallout