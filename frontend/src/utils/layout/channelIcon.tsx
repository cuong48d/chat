import { BiGlobe, BiHash, BiLockAlt } from 'react-icons/bi';
import { ChatChannel } from "../../../../types/ChatChannelManagement/ChatChannel";
import { IconBaseProps } from 'react-icons';

export const getChannelIcon = (type: ChatChannel['type']) => {

    switch (type) {
        case 'Private': return BiLockAlt
        case 'Open': return BiGlobe
        default: return BiHash
    }
}

interface ChannelIconProps extends IconBaseProps {
    type: ChatChannel['type']
}

export const ChannelIcon = ({ type, ...props }: ChannelIconProps) => {

    if (!type) return null

    if (type === 'Private') return <BiLockAlt {...props} />
    if (type === 'Open') return <BiGlobe {...props} />
    return <BiHash {...props} />

}
