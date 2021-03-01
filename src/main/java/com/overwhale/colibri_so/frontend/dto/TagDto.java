package com.overwhale.colibri_so.frontend.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import lombok.Data;

import javax.annotation.Nullable;
import javax.validation.constraints.NotNull;
import java.time.OffsetDateTime;
import java.util.UUID;

@Data
public class TagDto {
  @Nullable private UUID id;

  @Nullable
  @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss.SSSXXX")
  private OffsetDateTime creationTime;

  @Nullable
  @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss.SSSXXX")
  private OffsetDateTime lastChangedTime;

  @Nullable private UUID creatorId;

  @NotNull private String tag;

  @Nullable private String description;
}
