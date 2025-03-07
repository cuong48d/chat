import { Loader } from "@/components/common/Loader"
import BotForm from "@/components/feature/settings/ai/bots/BotForm"
import { ErrorBanner } from "@/components/layout/AlertBanner/ErrorBanner"
import { FullPageLoader } from "@/components/layout/Loaders/FullPageLoader"
import PageContainer from "@/components/layout/Settings/PageContainer"
import SettingsContentContainer from "@/components/layout/Settings/SettingsContentContainer"
import SettingsPageHeader from "@/components/layout/Settings/SettingsPageHeader"
import { HStack } from "@/components/layout/Stack"
import { ChatBot } from "@/types/ChatBot/ChatBot"
import { isEmpty } from "@/utils/validations"
import { Button } from "@radix-ui/themes"
import { useFrappeGetDoc, useFrappeUpdateDoc, SWRResponse, FrappeContext, FrappeConfig } from "frappe-react-sdk"
import { useContext, useEffect } from "react"
import { FormProvider, useForm } from "react-hook-form"
import { FiExternalLink } from "react-icons/fi"
import { useNavigate, useParams } from "react-router-dom"
import { toast } from "sonner"

type Props = {}

const ViewBot = (props: Props) => {

    const { ID } = useParams<{ ID: string }>()

    const { data, isLoading, error, mutate } = useFrappeGetDoc<ChatBot>("Chat Bot", ID)

    return (
        <PageContainer>
            <ErrorBanner error={error} />
            {isLoading && <FullPageLoader className="h-64" />}
            {data && <ViewBotContent data={data} mutate={mutate} />}
        </PageContainer>
    )
}

const ViewBotContent = ({ data, mutate }: { data: ChatBot, mutate: SWRResponse['mutate'] }) => {

    const { updateDoc, loading, error } = useFrappeUpdateDoc<ChatBot>()

    const methods = useForm<ChatBot>({
        disabled: loading,
        defaultValues: data
    })

    const { formState: { dirtyFields } } = methods

    const isDirty = !isEmpty(dirtyFields)


    const onSubmit = (data: ChatBot) => {
        updateDoc("Chat Bot", data.name, data)
            .then((doc) => {
                toast.success("Saved")
                methods.reset(doc)
                mutate(doc, { revalidate: false })
            })
    }

    useEffect(() => {

        const down = (e: KeyboardEvent) => {
            if (e.key === 's' && (e.metaKey || e.ctrlKey)) {
                e.preventDefault()
                methods.handleSubmit(onSubmit)()
            }
        }

        document.addEventListener('keydown', down)
        return () => document.removeEventListener('keydown', down)
    }, [])



    return <form onSubmit={methods.handleSubmit(onSubmit)}>
        <FormProvider {...methods}>
            <SettingsContentContainer>
                <SettingsPageHeader
                    title={data.bot_name}
                    headerBadges={isDirty ? [{ label: "Not Saved", color: "red" }] : undefined}
                    actions={<HStack>
                        <OpenChatButton bot={data} />
                        <Button type='submit' disabled={loading}>
                            {loading && <Loader className="text-white" />}
                            {loading ? "Saving" : "Save"}
                        </Button>
                    </HStack>}
                    breadcrumbs={[{ label: 'Agents', href: '../' }, { label: data.name, href: '', copyToClipboard: true }]}
                />
                <ErrorBanner error={error} />
                <BotForm isEdit={true} />
            </SettingsContentContainer>
        </FormProvider>
    </form>

}

const OpenChatButton = ({ bot }: { bot: ChatBot }) => {

    const { call } = useContext(FrappeContext) as FrappeConfig

    const navigate = useNavigate()

    const currentWorkspace = localStorage.getItem('chatLastWorkspace')

    const openChat = () => {
        call.post("chat.api.chat_channel.create_direct_message_channel", {
            user_id: bot.chat_user
        }).then((res) => {
            if (currentWorkspace) {
                navigate(`/${currentWorkspace}/${res.message}`)
            } else {
                navigate(`/channel/${res.message}`)
            }
        })
    }

    return <Button variant='surface' color='gray'
        type='button'
        className="not-cal" onClick={openChat}>
        Open Chat
        <FiExternalLink />
    </Button>
}

export const Component = ViewBot