package main

import (
	"encoding/json"
	"fmt"
	"os"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/sqs"
	"github.com/bwmarrin/discordgo"
)

const (
	queueName = "lynlab-tenri-discord"
	timeout   = 20
)

type DiscordMessage struct {
	ChannelName string `json:"channel_name"`

	Content string `json:"content"`
	Embed   *struct {
		Title       string `json:"title"`
		Description string `json:"description"`
		URL         string `json:"url"`
	} `json:"embed"`
}

func sendMessage(dg *discordgo.Session, msg *DiscordMessage) error {
	lynlabGuildID := os.Getenv("DISCORD_GUILD_ID")

	// Get ID of the channel
	channelID := ""
	channels, _ := dg.GuildChannels(lynlabGuildID)
	for _, channel := range channels {
		if channel.Name == msg.ChannelName {
			channelID = channel.ID
		}
	}

	if channelID == "" {
		return fmt.Errorf("invalid channel name")
	}

	// Send message
	input := &discordgo.MessageSend{Content: msg.Content}
	if msg.Embed != nil {
		input.Embed = &discordgo.MessageEmbed{
			Title:       msg.Embed.Title,
			Description: msg.Embed.Description,
			URL:         msg.Embed.URL,
		}
	}

	dg.ChannelMessageSendComplex(channelID, input)

	return nil
}

func main() {
	// Open discord connection
	dg, err := discordgo.New("Bot " + os.Getenv("DISCORD_BOT_TOKEN"))
	if err != nil {
		fmt.Println("Error creating discord session, ", err)
		return
	}

	err = dg.Open()
	if err != nil {
		fmt.Println("Error opening discord connection, ", err)
		return
	}

	// Open SQS session
	sess, err := session.NewSession(&aws.Config{
		Region: aws.String("ap-northeast-2"),
	})
	if err != nil {
		fmt.Println("Error opening SQS session, ", err)
		return
	}

	svc := sqs.New(sess)
	resultURL, err := svc.GetQueueUrl(&sqs.GetQueueUrlInput{
		QueueName: aws.String(queueName),
	})
	if err != nil {
		fmt.Println("Error getting result URL, ", err)
		return
	}
	

	// Long-poll sqs
	for {
		result, err := svc.ReceiveMessage(&sqs.ReceiveMessageInput{
			QueueUrl: resultURL.QueueUrl,
			AttributeNames: aws.StringSlice([]string{ "SentTimestamp" }),
			MaxNumberOfMessages: aws.Int64(1),
			MessageAttributeNames: aws.StringSlice([]string{ "All" }),
			WaitTimeSeconds: aws.Int64(timeout),
		})

		if err != nil {
			fmt.Println("Error receiving message, ", err)
		}

		if len(result.Messages) > 0 {
			msg := new(DiscordMessage)
			json.Unmarshal([]byte(*result.Messages[0].Body), &msg)

			go sendMessage(dg, msg)

			svc.DeleteMessage(&sqs.DeleteMessageInput{
				QueueUrl: resultURL.QueueUrl,
				ReceiptHandle: result.Messages[0].ReceiptHandle,
			})
		}
	}
}
