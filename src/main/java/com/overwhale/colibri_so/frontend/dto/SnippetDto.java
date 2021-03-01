package com.overwhale.colibri_so.frontend.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.overwhale.colibri_so.backend.entity.SnippetType;
import lombok.Data;

import javax.annotation.Nullable;
import javax.persistence.EnumType;
import javax.persistence.Enumerated;
import javax.validation.constraints.NotNull;
import java.time.OffsetDateTime;
import java.util.HashSet;
import java.util.Set;
import java.util.UUID;

@Data
public class SnippetDto {
  @Nullable private UUID id;

  @Nullable
  @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss.SSSXXX")
  private OffsetDateTime creationTime;

  @Nullable
  @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss.SSSXXX")
  private OffsetDateTime lastChangedTime;

  @Nullable
  private UUID creatorId;

  @Nullable private String content;

  @Nullable private String description;

  @Enumerated(EnumType.STRING)
  @NotNull
  private SnippetType snippetType;

  @Nullable private String mimetype;

  @Nullable private Integer favouriteLevel;

  @Nullable private String icon;

  @Nullable
  private Set<ProjectDto> projects = new HashSet<>();

  @Nullable
  private Set<TagDto> tags = new HashSet<>();

  @Nullable
  private Set<IntentDto> intents = new HashSet<>();
}
