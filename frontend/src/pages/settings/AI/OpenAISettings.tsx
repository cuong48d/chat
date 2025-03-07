import { ErrorText, HelperText, Label } from '@/components/common/Form'
import { Loader } from '@/components/common/Loader'
import PageContainer from '@/components/layout/Settings/PageContainer'
import SettingsContentContainer from '@/components/layout/Settings/SettingsContentContainer'
import SettingsPageHeader from '@/components/layout/Settings/SettingsPageHeader'
import useChatSettings from '@/hooks/fetchers/useChatSettings'
import { ChatSettings } from '@/types/Chat/ChatSettings'
import { hasChatAdminRole, isSystemManager } from '@/utils/roles'
import { Box, Button, Checkbox, Flex, Separator, Text, TextField } from '@radix-ui/themes'
import { useFrappeGetCall, useFrappeUpdateDoc } from 'frappe-react-sdk'
import { useEffect } from 'react'
import { Controller, FormProvider, useForm } from 'react-hook-form'
import { toast } from 'sonner'

const OpenAISettings = () => {

    const isChatAdmin = hasChatAdminRole() || isSystemManager()

    const { chatSettings, mutate } = useChatSettings()

    const methods = useForm<ChatSettings>({
        disabled: !isChatAdmin
    })

    const { handleSubmit, control, watch, reset, register, formState: { errors } } = methods

    useEffect(() => {
        if (chatSettings) {
            reset(chatSettings)
        }
    }, [chatSettings])

    const { updateDoc, loading: updatingDoc } = useFrappeUpdateDoc<ChatSettings>()

    const onSubmit = (data: ChatSettings) => {
        toast.promise(updateDoc('Chat Settings', null, {
            ...(chatSettings ?? {}),
            ...data
        }).then(res => {
            mutate(res, {
                revalidate: false
            })
        }), {
            loading: 'Updating...',
            success: () => {
                return `Settings updated`;
            },
            error: 'There was an error.',
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

    const isAIEnabled = watch('enable_ai_integration')

    const { data: openaiVersion } = useFrappeGetCall<{ message: string }>('chat.api.ai_features.get_open_ai_version')

    return (
        <PageContainer>
            <FormProvider {...methods}>
                <form onSubmit={handleSubmit(onSubmit)}>
                    <SettingsContentContainer>
                        <SettingsPageHeader
                            title='OpenAI Settings'
                            description='Set your OpenAI API Key to use AI features in Chat.'
                            actions={<Button type='submit' disabled={updatingDoc || !isChatAdmin}>
                                {updatingDoc && <Loader className="text-white" />}
                                {updatingDoc ? "Saving" : "Save"}
                            </Button>}
                        />

                        <Flex direction={'column'} gap='2'>
                            <Text as="label" size="2">
                                <Flex gap="2">
                                    <Controller
                                        control={control}
                                        defaultValue={chatSettings?.enable_ai_integration}
                                        name='enable_ai_integration'
                                        render={({ field }) => (
                                            <Checkbox
                                                checked={field.value ? true : false}
                                                name={field.name}
                                                disabled={field.disabled}
                                                onCheckedChange={(v) => field.onChange(v ? 1 : 0)}
                                            />
                                        )} />

                                    Enable AI Integration
                                </Flex>
                            </Text>
                        </Flex>
                        <Separator size='4' />
                        {isAIEnabled ?
                            <Box>
                                <Label htmlFor='openai_organisation_id' isRequired>OpenAI Organization ID</Label>
                                <TextField.Root
                                    autoFocus
                                    maxLength={140}
                                    className={'w-48 sm:w-96'}
                                    id='openai_organisation_id'
                                    autoComplete='off'
                                    required
                                    placeholder='org-************************'
                                    {...register('openai_organisation_id', {
                                        required: isAIEnabled ? "Please add your OpenAI Organization ID" : false,
                                        maxLength: {
                                            value: 140,
                                            message: "ID cannot be more than 140 characters."
                                        }
                                    })}
                                    aria-invalid={errors.openai_organisation_id ? 'true' : 'false'}
                                />
                                {errors?.openai_organisation_id && <ErrorText>{errors.openai_organisation_id?.message}</ErrorText>}
                            </Box>
                            : null
                        }

                        {isAIEnabled ?
                            <Box>
                                <Label htmlFor='openai_api_key' isRequired>OpenAI API Key</Label>
                                <TextField.Root
                                    className={'w-48 sm:w-96'}
                                    id='openai_api_key'
                                    required
                                    type='password'
                                    autoComplete='off'
                                    placeholder='••••••••••••••••••••••••••••••••'
                                    {...register('openai_api_key', {
                                        required: isAIEnabled ? "Please add your OpenAI API Key" : false,
                                    })}
                                    aria-invalid={errors.openai_api_key ? 'true' : 'false'}
                                />
                                {errors?.openai_api_key && <ErrorText>{errors.openai_api_key?.message}</ErrorText>}
                            </Box>
                            : null
                        }

                        {isAIEnabled ?
                            <Box>
                                <Label htmlFor='openai_project_id'>OpenAI Project ID</Label>
                                <TextField.Root
                                    maxLength={140}
                                    className={'w-48 sm:w-96'}
                                    id='openai_project_id'
                                    autoComplete='off'
                                    placeholder='proj_************************'
                                    {...register('openai_project_id', {
                                        maxLength: {
                                            value: 140,
                                            message: "ID cannot be more than 140 characters."
                                        }
                                    })}
                                    aria-invalid={errors.openai_project_id ? 'true' : 'false'}
                                />
                                {errors?.openai_project_id && <ErrorText>{errors.openai_project_id?.message}</ErrorText>}
                                <HelperText>
                                    If not set, the integration will use the default project.
                                </HelperText>
                            </Box>
                            : null
                        }

                        {openaiVersion && <Text color='gray' size='2'>OpenAI Python SDK Version: {openaiVersion.message}</Text>}
                    </SettingsContentContainer>
                </form>
            </FormProvider>
        </PageContainer>
    )
}

export const Component = OpenAISettings